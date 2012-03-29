#!/usr/bin/python3
# File Name: DeletedLines.py

# This file contains only the useless deleted line from other .py files.


class Error(Exception):
	"""Base class for exceptions in this module"""
	pass

class SameNumberError(Error):
	"""Exception raised by inputing same StuffNumber

	Attributes:
		message -- explanation of the error"""
	def __init__(self, value, message):
		self.value = value
		self.message = message
