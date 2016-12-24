# data_parsing.py
# Expects an input directory containing player data files as formatted on liquipedia
# Will produce json documents containing key value pairs, along with player history

import os, re
from operator import itemgetter
from parse import *
from pymongo import MongoClient
import time

# Start at the most recent entry
# check for present, then leave as is
# if ? in end date, round ?? fields up
# if ? in start date, refer to the previous entry
def fix_history(history):
	history_list = []
	# This could be more pythonic
	for entry in history:
		history_list.extend(entry[:2])
	history_list.reverse()
	# Since history list is reversed (most recent at the beginning)
	print("history object: " + str(history))
	print("history_list: " + str(history_list))
	end_list = []
	for index, date in enumerate(history_list):
		print(str(index) + " " + str(date))
		if '?' in date:
			if index == 0:
				print("First date has ambiguity")
				end_list.append(round_date(date, "2017-12-31", False))
			elif index == len(history_list) - 1:
				print("Final date has ambiguity")
				end_list.append(round_date(date, "2010-01-01", True))
			else:
				# examine surrounding dates and put into that context
				end_list.append(date_context(history_list[index - 1: index + 2], index % 2 == 0))
		else:
			end_list.append(date)

	end_list.reverse()
	# Read data back into history object
	for index in range(len(end_list)):
		history[index // 2][index % 2] = end_list[index]
	# Appears that no entries are added to history list after '?' is encountered
	print("end_list" + str(end_list))
	print("history_final:" + str(history))
	print("\n\n\n")

# reverse the history
# ensure the most recent team end date is properly formatted
	# round missing fields up to 2017-12-30
# check start date for problems
	# if problem, check that team-1[end] is proper
	# if proper, then round towards that date? (round month/day down)
	# If both problem, round team[start] down to start of month (guess)

	# fix each tuple sequentially, starting with the most recent team
	# Look 

# Accept a list of integers representing a date (xxxx-xx-xx)
# Calcualte the day before, unless its February, then fuck off, there is a 31st
def day_before(date):
	date[2] -= 1
	if date[2] == 0:
		date[1] -= 1
		date[2] = 31
		if date[1] == 0:
			date[1] = 12
			date[0] -= 1
	return date

# If lower bound date is ambiguous, then round up to the upper bound date
# if both dates are certain, then work to maximize the span of time on a team
# Do not forget to cast the ints to print in two digits
def date_context(date_list, leave):
	date_compare = date_list[1].split('-')
	future_date_compare = list(map(int, date_list[0].split('-')))
	past_date = date_list[2]

	# Uncertainty exists on the lower bounding date
	# I do not care about the month of February
	if '?' in past_date:
		# Check what fields of the estimating date and the future date agree
		# If the year is ambiguous
		if '?' in date_compare[0]:
			return "{}-{}-{}".format(*day_before(future_date_compare))
		# If the month is ambiguous
		elif '?' in date_compare[1]:
			# if the year is the same
			if future_date_compare[0] == int(date_compare[0]):
				return "{}-{}-{}".format(*day_before(future_date_compare))
			else:
				# Round to the end of the year
				return "{}-{}-{}".format(date_compare[0], "12", "31")
		# If the day is ambiguous
		elif '?' in date_compare[2]:
			# If the month is the same
			if future_date_compare[1] == int(date_compare[1]):
				return "{}-{}-{}".format(*day_before(future_date_compare))
			else:
				# Round to the end of the month
				return "{}-{}-{}".format(date_compare[0], date_compare[1], "31")
	else:
		if leave:
			return "{}-{}-{}".format(*day_before(future_date_compare))
		else:
			future_date_compare[2] += 2
			if future_date_compare[2] > 31:
				future_date_compare[2] = future_date_compare[2] % 31
				future_date_compare[1] += 1
				if future_date_compare[1] > 12:
					future_date_compare[1] = future_date_compare[1] % 12
					future_date_compare[0] += 1
			return "{}-{}-{}".format(*future_date_compare)

# probably need to just rewrite this in a different manner, compare each field for low/high
def round_date(date, target, up):
	rounder_fxns = {True: max, False: min}
	rounder = rounder_fxns[up]
	target = target.split('-')
	date_separated = date.replace('??', '99').split('-')
	try:
		ret_date = "{}-{}-{}".format(rounder(int(target[0]), int(date_separated[0])), rounder(int(target[1]), int(date_separated[1])), rounder(int(target[2]), int(date_separated[2])))
	except:
		# Create proper exception handling format here
		print("Error in rounding date, target:" + str(date) + ", " + str(target))
		raise
	return ret_date

db_client = MongoClient()
db = db_client.dota
db.players.remove()

# Set directory parameters
DATA_DIRECTORY = "data/"
RESULTS_DIRECTORY = "results/"

# Establish a file for tracking pages that cause issues, mostly personalities
nil_history_pages = open(RESULTS_DIRECTORY + "0_error_pages.txt", 'w')
history_error_pages = open(RESULTS_DIRECTORY + "0_history_error_pages.txt", 'w')

for file_name in os.listdir(DATA_DIRECTORY):
	# If an error is detected, do not add to the databse
	error = False
	try:
		# Read incoming data
		input_file = open(DATA_DIRECTORY + file_name)
		body = input_file.read()
		input_file.close()

		# Remove extraneous points of data such as html headers
		removed_top = body.split("{{Infobox player")[1].split("|history=")
		simple_vars = removed_top[0]
		history = removed_top[1].rpartition("}}")[0]
	except IndexError:
		# These files had no history listed
		error = True
		nil_history_pages.write(file_name + "\n")

	# Retrieve the key value pairs in the nonstandard data format
	player_attrs = {}
	for line in simple_vars.split("\n"):
		if '=' in line:
			key_value_pair = line.replace('|', '',1).split("=")
			if key_value_pair[1]:
				player_attrs.update({key_value_pair[0]: key_value_pair[1]})

	player_attrs['history'] = []
	# Obtain the history of the players, using parse to retrieve the data
	# This method is not robust, but I don't feel like learning regex at the moment
	# A number of None entries are appearing, due to nonstandard data formats
	for line in history.split("\n"):
		if "{{TH|" in line:
			line = line.replace('{', '').replace('}', '')
			history_element = None
			# Account for hypen dash discrepencies
			if '—' in line:
				# http://stackoverflow.com/questions/11844986/convert-string-to-variables-like-format-but-in-reverse-in-python
				history_element = parse("TH|{} — {}|{}", line)
			else:
				history_element = parse("TH|{} - {}|{}", line)
			if history_element:
				# Replace the string present in the history tuple with the current date
				entry = [history_element[0], history_element[1] if not 'present' in history_element[1].lower() else time.strftime("%Y-%m-%d") , history_element[2], '?' in history_element[0], '?' in history_element[1]]
				if not True in entry:
					player_attrs['history'].append(entry)
				else:
					# If there is ambiguity in the dates, then simply ignore them for now
					# There is logic at the top of this file to try to fix it but I am ignoring it for now
					history_error_pages.write("single line error in " + file_name + ":" + line + "\n")
			else:
				# Does not appear to be activated in the dataset, but going to keep
				history_error_pages.write(file_name + " no history element:" + line + "\n")
				error = True

	if not error:
		db.players.insert(player_attrs)
		print(player_attrs['history'])

history_error_pages.close()
nil_history_pages.close()
