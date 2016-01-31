#!/usr/bin/env python3


import argparse
import os
import shutil
import sys

sys.path.insert(0, "Scripts")
import Common.package_s3 as package


def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("--environment", required=True, help="target environment")
	return parser.parse_args()


if __name__ == "__main__":
	arguments = parse_arguments()
	
	print("Checking active package on environment " + arguments.environment)
	package_file = package.get_active("MyWebsite", arguments.environment)
	
	print("Downloading package " + package_file)
	package.download("MyWebsite", package_file)

	try:
		shutil.unpack_archive(package_file, "MyWebsite_new")
		shutil.rmtree("MyWebsite")
		os.rename("MyWebsite_new", "MyWebsite")
	finally:
		os.remove(package_file)