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

sys.path.insert(0, "Scripts")
import Common.lock
import Common.package_filesystem as package

sys.path.insert(0, "Project")
import project


PACKAGE_DIRECTORY = "../../Packages"


def clean():
	print("=== Clean up ===")
	if os.path.exists("Deploy"):
		shutil.rmtree("Deploy")
	print()


def deploy():
	print("=== Deployment ===")

	print("Create package")
	if os.path.exists("Deploy") == False:
		os.mkdir("Deploy")
	shutil.make_archive("Deploy/example", "zip", "Output")

	print("Deploy package to repository")
	package.upload("Example", "Deploy/example.zip")
	print()


if __name__ == "__main__":

	with Common.lock.lock_directory(""):

		clean()
		
		project.clean()
		project.build()
		project.validate()
		
		deploy()

		# Foreach instance
		#	Remote connect and execute update script
		# OR
		#	Launch new instance