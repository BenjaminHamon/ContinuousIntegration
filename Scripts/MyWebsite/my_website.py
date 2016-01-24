#!/usr/bin/env python3


import os
import shutil
import sys

sys.path.insert(0, "Scripts/Common")
import lock

sys.path.insert(0, "Project")
import MyWebsite


PACKAGE_DIRECTORY = "../../Packages"


def clean():
	print("=== Clean up ===")
	if os.path.exists("deploy"):
		shutil.rmtree("deploy")


def deploy():
	print("=== Deployment ===")

	print("Create package")
	if os.path.exists("deploy") == False:
		os.mkdir("deploy")
	shutil.make_archive("deploy/my_website", "zip", "Project/MyWebsite/Publish/" + configuration)

	print("Deploy package to repository")
	package_directory = os.path.join(PACKAGE_DIRECTORY, "MyWebsite")
	if os.path.exists(package_directory) == False:
		os.mkdir(package_directory)
	shutil.copy("deploy/my_website.zip", package_directory)


if __name__ == "__main__":
	with lock.lock_directory(""):
		clean()
		print()
		
		configuration = "Debug"
		verbose = False
		
		MyWebsite.verbose = verbose
		MyWebsite.configuration = configuration
		
		os.chdir("Project")
		
		try:
			MyWebsite.clean()
			print()

			MyWebsite.build()
			print()

			MyWebsite.validate()
			print()

			MyWebsite.publish()
			print()
			
		finally:
			os.chdir("../")

		deploy()

		# Foreach instance
		#	Remote connect and execute update script
		# OR
		#	Launch new instance