#!/usr/bin/env python3


import os

import boto3 # AWS

s3 = boto3.resource("s3")


PACKAGE_BUCKET = "bhamon-packages"

bucket = s3.Bucket(PACKAGE_BUCKET)


def download(project, package):
	bucket.download_file(project + "/" + package, package)


def upload(project, package):
	package_name = os.path.basename(package)
	bucket.upload_file(package, project + "/" + package_name)
	
	
def get_active(project, environment):
	request = boto3.client("s3").get_object(Bucket = PACKAGE_BUCKET, Key = project + "/" + environment + ".active.txt")
	return request["Body"].read().decode("utf-8")
	
	
def set_active(project, package, environment):
	bucket.put_object(Key = project + "/" + environment + ".active.txt", Body = package.encode("utf-8"))
	
	