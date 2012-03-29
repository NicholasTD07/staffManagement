#!/usr/bin/python3
# File Name: Functions.py

# This file has the functions defined inside it.

import StuffClass

def Generator(StuffNumbers, Gender='Male', Shift='Day'):
	"""This Function Generates the needed Stuffs according to the input.

	Keyword Arguments:
		StuffNumbers -- A list contains the StuffNumber for each stuff.
		Gender -- The Gender of the stuff.
		Shift -- Which Shift the stuff take.
	"""

	for StuffNumber in StuffNumbers:
		#global StuffID
		StuffID = Shift+'Shift_'+'{0}'.format(StuffNumber)
		print("{0}".format(StuffID))
		globals()[StuffID] = StuffClass.AllStuff(StuffNumber, Gender, Shift)

if __name__ == '__main__':
	Generator([1,3,5,7,9,11])
	Generator([2,4,6,8,10,12],'Female','Night')
	DayShift_1.Work()
	DayShift_1.Work()
	NightShift_2.Work()
	DayShift_3.Work()
	NightShift_4.Work()
	NightShift_6.Work()
	DayShift_3.Work()
	NightShift_4.Work()
	print("AllTimes")
	DayShift_1.AllTimes()
	DayShift_1.Details()
