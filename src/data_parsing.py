import os

DATA_DIRECTORY = "data/"

for file_name in os.listdir(DATA_DIRECTORY):
	try:
		file = open(DATA_DIRECTORY + file_name)
		body = file.read()
		history_half = body.split("history=")[1]
		print(history_half)
	except IndexError:
		print(file_name + " does not contain a history element")
