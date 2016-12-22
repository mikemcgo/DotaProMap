import os, re
from operator import itemgetter
from parse import *

DATA_DIRECTORY = "data/"
RESULTS_DIRECTORY = "results/"

nil_history_pages = open(RESULTS_DIRECTORY + "0_error_pages.txt", 'w')
for file_name in os.listdir(DATA_DIRECTORY):
	try:
		input_file = open(DATA_DIRECTORY + file_name)
		body = input_file.read()
		input_file.close()
		removed_top = body.split("{{Infobox player")[1].split("|history=")
		simple_vars = removed_top[0]
		history = removed_top[1].rpartition("}}")[0]
		# history parsing, will parse all vars for db sake
		player_attrs = {}
		for line in simple_vars.split("\n"):
			if '=' in line:
				key_value_pair = line.replace('|', '',1).split("=")
				player_attrs.update({key_value_pair[0]: key_value_pair[1]})

		print(file_name)
		for line in history.split("\n"):
			# http://stackoverflow.com/questions/11844986/convert-string-to-variables-like-format-but-in-reverse-in-python
			if "{{TH|" in line:
				line = line.replace('{', '').replace('}', '')
				m = parse("TH|{} — {}|{}", line)
				print(m)

		# establish known problem names file, and check against it
		# run a normal parse (assume resonable data)
		# Attempt to account for dota1/starcraft data
		# push unparseable data to files to be manually edited
	except IndexError:
		# These files had no history listed
		nil_history_pages.write(file_name + "\n")

nil_history_pages.close()
