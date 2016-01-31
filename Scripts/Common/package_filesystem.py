#!/usr/bin/env python3


import os
import shutil


# TODO: Replace with environment variable
PACKAGE_DIRECTORY = "../../Packages"


def upload(project, package):
	package_directory = os.path.join(PACKAGE_DIRECTORY, project)
	if os.path.exists(package_directory) == False:
		os.mkdir(package_directory)
	shutil.copy(package, package_directory)