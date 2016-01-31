#!/usr/bin/env python3


import os

import boto3 # AWS

s3 = boto3.resource("s3")


PACKAGE_BUCKET = "bhamon-packages"

bucket = s3.Bucket(PACKAGE_BUCKET)


def upload(project, package):
	package_name = os.path.basename(package)
	with open(package, "rb") as package_data:
		bucket.put_object(Key = project + "/" + package_name, Body = package_data)