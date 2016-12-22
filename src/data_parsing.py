# data_parsing.py
# Expects an input directory containing player data files as formatted on liquipedia
# Will produce json documents containing key value pairs, along with player history

import os, re
from operator import itemgetter
from parse import *

# Set directory parameters
DATA_DIRECTORY = "data/"
RESULTS_DIRECTORY = "results/"

# Establish a file for tracking pages that cause issues, mostly personalities
nil_history_pages = open(RESULTS_DIRECTORY + "0_error_pages.txt", 'w')

for file_name in os.listdir(DATA_DIRECTORY):
	try:
		# Read incoming data
		input_file = open(DATA_DIRECTORY + file_name)
		body = input_file.read()
		input_file.close()

		# Remove extraneous points of data such as html headers
		removed_top = body.split("{{Infobox player")[1].split("|history=")
		simple_vars = removed_top[0]
		history = removed_top[1].rpartition("}}")[0]

		# Retrieve the key value pairs in the nonstandard data format
		player_attrs = {}
		for line in simple_vars.split("\n"):
			if '=' in line:
				key_value_pair = line.replace('|', '',1).split("=")
				player_attrs.update({key_value_pair[0]: key_value_pair[1]})

		# Obtain the history of the players, using parse to retrieve the data
		# This method is not robust, but I don't feel like learning regex at the moment
		# A number of None entries are appearing, due to nonstandard data formats (270/3972 lines are bad)
		for line in history.split("\n"):
			# http://stackoverflow.com/questions/11844986/convert-string-to-variables-like-format-but-in-reverse-in-python
			if "{{TH|" in line:
				line = line.replace('{', '').replace('}', '')
				m = parse("TH|{} — {}|{}", line)
				print(m)

		# run a normal parse (assume resonable data)
		# Attempt to account for dota1/starcraft data
		# push unparseable data to files to be manually edited
	except IndexError:
		# These files had no history listed
		nil_history_pages.write(file_name + "\n")

nil_history_pages.close()
