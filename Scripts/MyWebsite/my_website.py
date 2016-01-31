#!/usr/bin/env python3


import argparse
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, "Scripts")
import Common.lock
import Common.os_extensions
import Common.package_s3 as package


def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("--activate", action="store_true", help="activate the deployed package, replacing the previous one")
	parser.add_argument("--configuration", required=True, help="configuration file to load")
	parser.add_argument("--environment", required=True, help="target environment")
	parser.add_argument("--revision", required=True, help="sources revision to check out")
	parser.add_argument("--verbose", action="store_true", help="increase output verbosity")
	return parser.parse_args()


def clean():
	print("=== Clean up ===")
	if os.path.exists("Deploy"):
		shutil.rmtree("Deploy")
	print()


def update_sources(url, revision):
	print("=== Sources ===")
	print("Updating repository to revision " + revision)
	if os.path.exists("Project") == False:
		subprocess.check_call("git clone -q " + url + " Project")
	with Common.os_extensions.change_directory("Project"):
		subprocess.check_call("git fetch")
		revision = subprocess.check_output("git rev-parse --verify origin/" + revision).decode("utf-8").strip()
		subprocess.check_call("git checkout " + revision)
	print()
	return revision


def deploy(build_configuration, revision, activate, environment):
	print("=== Deployment ===")

	if os.path.exists("Deploy") == False:
		os.mkdir("Deploy")
	package_name = "my_website-" + revision
		
	print("Creating package " + package_name)
	shutil.make_archive("Deploy/" + package_name, "zip", "Project/MyWebsite/Publish/" + build_configuration)

	print("Deploying package to repository")
	package.upload("MyWebsite", "Deploy/" + package_name + ".zip")
	
	if activate:
		print("Activating package on environment " + environment)
		package.set_active("MyWebsite", package_name + ".zip", environment)
	
	print()


if __name__ == "__main__":
	arguments = parse_arguments()
	with open("Configuration/MyWebsite/" + arguments.configuration) as configuration_file:    
		configuration = json.load(configuration_file)

	with Common.lock.lock_directory(""):
		clean()
		revision = update_sources(configuration["sources"]["url"], arguments.revision)

		sys.path.insert(0, "Project")
		import MyWebsite
		
		with Common.os_extensions.change_directory("Project"):
			MyWebsite.verbose = arguments.verbose
			MyWebsite.configuration = configuration["build"]["configuration"]
			
			MyWebsite.clean()
			MyWebsite.build()
			MyWebsite.validate()
			MyWebsite.publish()

		deploy(configuration["build"]["configuration"], revision, arguments.activate, arguments.environment)

		# Foreach instance
		#	Remote connect and execute update script
		# OR
		#	Launch new instance