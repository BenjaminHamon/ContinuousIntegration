#!/usr/bin/env python3


from contextlib import contextmanager
import os


@contextmanager
def lock_directory(path):
	lock_path = os.path.join(path, "lock")
	if os.path.exists(lock_path):
		raise Exception("[Error] Directory is locked")
	open(lock_path, "w+").close()
	try:
		yield
	finally:
		os.remove(lock_path)
