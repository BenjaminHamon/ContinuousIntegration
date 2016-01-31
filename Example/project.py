#!/usr/bin/env python3


import argparse
import os
import shutil


def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("--action", default="", required=True, help="action(s) to execute on the project, separated by comma")
	parser.add_argument("--environment", default="local", required=False, help="target environment")
	return parser.parse_args()

	
def execute_actions(actionList):
	actionDictionary = {
		"clean": clean,
		"build": build,
		"validate": validate,
	}
	
	for action in actionList:
		actionDictionary[action]()


def clean():
	print("=== Clean up ===")
	if os.path.exists("Output"):
		shutil.rmtree("Output")
	print()


def build():
	print("=== Build ===")
	
	if os.path.exists("Output") == False:
		os.mkdir("Output")
		
	print("Create project file")
	file = open("Output/example.txt", "w+")
	print()


def validate():
	print("=== Validation ===")
	if os.path.exists("Output/example.txt"):
		print("Success")
	else:
		raise Exception("Validation failed")
	print()


if __name__ == "__main__":
	base_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	os.chdir(base_directory)
	
	arguments = parse_arguments()
	actionList = arguments.action.split(",")
	execute_actions(actionList)