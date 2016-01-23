#!/usr/bin/env python3

import os
import shutil
import sys
sys.path.insert(0, "project/scripts")

import project


PACKAGE_DIRECTORY = "packages"


def clean():
	print("=== Clean up ===")
	if os.path.exists("deploy"):
		shutil.rmtree("deploy")


def deploy():
	print("=== Deployment ===")
	
	print("Create package")
	if os.path.exists("deploy") == False:
		os.mkdir("deploy")
	shutil.make_archive("deploy/example", "zip", "output")
	
	print("Deploy package to repository")
	package_directory = os.path.join(PACKAGE_DIRECTORY, "example")
	if os.path.exists(package_directory) == False:
		os.mkdir(package_directory)
	shutil.copy("deploy/example.zip", package_directory)


if __name__ == "__main__":
	base_directory = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
	os.chdir(base_directory)
	
	# Package repository should already exists.
	# For the example we create it ourselves.
	if os.path.exists(PACKAGE_DIRECTORY) == False:
		os.mkdir(PACKAGE_DIRECTORY)

	clean()
	project.clean()
	print()
	
	project.build()
	print()
	
	project.validate()
	print()
	
	deploy()