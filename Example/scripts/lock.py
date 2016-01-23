#!/usr/bin/env python3


import os


def lock_directory(path):
	lock_path = os.path.join(path, "lock")
	if os.path.exists(lock_path):
		raise Exception("[Error] Directory is locked")
	file = open(lock_path, "w+")


def unlock_directory(path):
	lock_path = os.path.join(path, "lock")
	if os.path.exists(lock_path) == False:
		print("[Warning] Directory is not locked")
	else:
		os.remove(lock_path)