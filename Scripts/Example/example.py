#!/usr/bin/env python3

# Continuous integration script for the Example project.

# Summary
#	Cleans the workspace
#	Builds the project
#	Validates the project output
#	Packages the project ouput
#	Deploys the package to the repository
#	Updates instances or launches new ones.


import os
import shutil
import sys

sys.path.insert(0, "Scripts/Common")
import lock

sys.path.insert(0, "Project")
import project


PACKAGE_DIRECTORY = "../../Packages"


def clean():
	print("=== Clean up ===")
	if os.path.exists("Deploy"):
		shutil.rmtree("Deploy")


def deploy():
	print("=== Deployment ===")

	print("Create package")
	if os.path.exists("Deploy") == False:
		os.mkdir("Deploy")
	shutil.make_archive("Deploy/example", "zip", "Output")

	print("Deploy package to repository")
	package_directory = os.path.join(PACKAGE_DIRECTORY, "Example")
	if os.path.exists(package_directory) == False:
		os.mkdir(package_directory)
	shutil.copy("Deploy/example.zip", package_directory)


if __name__ == "__main__":

	with lock.lock_directory(""):

		clean()
		print()
		
		project.clean()
		print()

		project.build()
		print()

		project.validate()
		print()

		deploy()

		# Foreach instance
		#	Remote connect and execute update script
		# OR
		#	Launch new instance