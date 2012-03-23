#!/usr/bin/python
# Fliename: StuffClass.py

# This file defines the class for all stuff and some methods.

#import pickle, time

# First we need a class for AllStuff
# Need: 1. DayShift or NightShift
#		2. WorkTimes
#		3. StuffNumber
#		4. Gender


class AllStuff:
	""" This is the parent class for DayShift and NightShift.

		DataStructure:
			Class variable:
				HowManyStuff  -- don't know how to solve the repeat problem
							  -- SOVLED
					It contains the number of all stuff together.
					And it is shared by DayShift and NightShift.
					It increases when there is a new instance.
			Instance variables:
			( The AllStuff Class has these instance variables )
				StuffNumber --  the stuff number -- Keyword arguments
				Shift -- the shift for the stuff -- Keyword arguments
				Gender -- the gender of the stuff -- Keyword arguments
				WorkType -- work type of this time

				WorkTimes -- how many time this stuff worked -- Calculated 
						  -- Do I Need To Be More Specifc?
						  -- Maybe A WorkTimes Class?
	"""

	HowManyStuff = 0
	StuffList = []
	NumberList = []
	#WorkTimes = {}

	def __init__(self, StuffNumber, Gender, Shift):
		if StuffNumber in AllStuff.NumberList:
			print("""Already had this Number.

		If you want to change the information of the stuff,
		please use the Chage Method.
			""")
		else:
			self.StuffNumber = StuffNumber
			self.Shift = Shift
			self.Gender = Gender
			self.WorkTimes = 0
			self.WorkType = None

			AllStuff.HowManyStuff += 1
			AllStuff.StuffList.append(self)
			AllStuff.NumberList.append(self.StuffNumber)
			#AllStuff.WorkTimes[self.StuffNumber] = (self.WorkTimes, self.WorkType)
			print("""Initialized Stuff: {0}""".format(self.StuffNumber))
			print("(All Stuff Numbers:{0})".format(AllStuff.NumberList))

	def AllTimes(self):
		#for stuff, (times, Type) in AllStuff.WorkTimes.items():
		for Stuff in AllStuff.StuffList:
			print("""No.{0} Stuff Last Time's work type is {2}
			Worked {1} time(s).""".		\
			format(Stuff.StuffNumber, Stuff.WorkTimes, Stuff.WorkType))
		print("\nTotally we have {0} Stuffs.".format(AllStuff.HowManyStuff))
		print("The Number List looks like {0}.\n".format(AllStuff.NumberList))

	def Work(self, WorkType='Normal'):
		self.WorkTimes += 1
		self.WorkType = WorkType
		#AllStuff.WorkTimes[self.StuffNumber] = (self.WorkTimes, self.WorkType)
		print("No.{0} today worked {1} time(s)".format(self.StuffNumber,self.WorkTimes))

	def Details(self):
		'''This Function tells the information of the Stuff.'''
		print("StuffNumber: {0}".format(self.StuffNumber))
		print("Shift: {0}".format(self.Shift))
		print("WorkTimes: {0}".format(self.WorkTimes))
		print("Gender: {0}".format(self.Gender))
		print("Last WorkType: {0}".format(self.WorkType))

class DayShift(AllStuff):
	""" This is the class for the DayShift.
		It has 
			__init__
			Work -- add the time this stuff work ONLY
	"""

	HowManyDayStuff = 0
	DayStuffList = []

	def __init__(self, StuffNumber, Gender):
		""" This is exactly the same as AllStuff except for 
			the Shift is defined default to Day.
		"""
		AllStuff.__init__(self,StuffNumber, Gender, "Day")
		DayShift.HowManyStuff += 1
		DayShift.DayStuffList.append(self)


	def Work(self):
		AllStuff.Work(self)

	def Details(self):
		AllStuff.Details(self)

class NightShift(AllStuff):
	""" This is the class for the NightShift.
		It has 
			__init__ -- 
			Work -- add the time this stuff work ONLY
	"""

	HowManyNgihtStuff = 0
	NightStuffList = []

	def __init__(self, StuffNumber, Gender):
		""" This is exactly the same as AllStuff except for 
			the Shift is defined default to Night.
		"""
		AllStuff.__init__(self,StuffNumber, Gender, "Night")
		NightShift.HowManyNgihtStuff += 1
		NightShift.NightStuffList.append(self)

	def Work(self):
		AllStuff.Work(self)

	def Details(self):
		AllStuff.Details(self)
