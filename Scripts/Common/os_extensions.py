#!/usr/bin/env python3


import contextlib
import os


@contextlib.contextmanager
def change_directory(new_directory):
	previous_directory = os.getcwd()
	os.chdir(new_directory)
	try:
		yield
	finally:
		os.chdir(previous_directory)