#!/usr/bin/python3
# File Name: StuffClass2.py

# Classes:
#	StuffInfo, WorkStatus, AllStuff, DayShift, NightShift

class StuffInfo:
	"The info of every stuff including StuffNumber, Gender, Shift."

	StuffNumberList = []
	def __init__(self, StuffNumber, Gender, Shift):
		if StuffNumber in StuffInfo.StuffNumberList:
			print("已有该工号,请检查后重新输入.")
		else:
			self.StuffNumber = StuffNumber
			self.Gender = Gender
			self.Shift = Shift
			StuffInfo.StuffNumberList.append(self.StuffNumber)

class WorkStatus:
	"""The current work status of the stuff including 
	
	WorkStatus -- 'Work' 'Wait'
	WorkedTimes -- More than 0
	WorkType -- 'Normal' 'Selected' 'Named'
	WaitPOS -- Position in the wait list
	WorkPOS -- Position in the working list
	"""
	MaxWorkTimes = 0
	NormalWorkList = {}
	NormalWorkPOS = 1
	SelectedWorkList = {}
	SelectedPOS = 0

	def __init__(self):
		self.WorkStatus = 'Wait'
		self.WorkedTimes = 0
		self.WorkType = None
		self.WaitPOS = None
		self.WorkPOS = None

	def Wait(self, WaitPOS):
		"""Needed Argument: WaitPOS.

		It also sets WorkPOS and WorkType to None
		"""
		self.WaitPOS = WaitPOS
		self.WorkPOS = None		# If Waiting Then not working
		self.WorkType = None

	def Work(self, WorkType):
		"""Needed Arguments: Worktype WorkPOS.
		
		It sets WaitPOS to None.
		"""
		self.WorkType = WorkType

		if self in WaitList.values() :
			pass
		else:
			#print("{0} 号员工不在等待上班状态.".format(self.StuffNumber))
			#print("{0} 号员工所属班组为 {1}.".format(self.StuffNumber, self.Shift))
			raise TypeError("{0} 号员工不在等待上班状态.\n {0} 号员工所属班组为 {1}".\
			format(self.StuffNumber,self.Shift))

		if self.WorkType == 'Normal':
			self.WorkPOS = WorkStatus.NormalWorkPOS
			WorkStatus.NormalWorkPOS += 1
			#WorkStatus.NormalWorkList[self.WorkPOS] = self.StuffNumber
			WorkStatus.NormalWorkList[self.WorkPOS] = self
		elif self.WorkType == 'Named':
			if WorkStatus.SelectedWorkList:
				self.WorkPOS = WorkStatus.SelectedPOS
				WorkStatus.SelectedPOS += 1
				#WorkStatus.SelectedWorkList[self.WorkPOS] = self.StuffNumber
				WorkStatus.SelectedWorkList[self.WorkPOS] = self
			else:
				self.WorkPOS = WorkStatus.NormalWorkPOS
				WorkStatus.NormalWorkPOS += 1
				#WorkStatus.NormalWorkList[self.WorkPOS] = self.StuffNumber
				WorkStatus.NormalWorkList[self.WorkPOS] = self
		elif self.WorkType == 'Selected':
			self.WorkPOS = self.WaitPOS
			WorkStatus.SelectedPOS = self.WorkPOS + 1
			#WorkStatus.SelectedWorkList[self.WorkPOS] = self.StuffNumber
			WorkStatus.SelectedWorkList[self.WorkPOS] = self
		else:
			print("输入的工作类型错误")
			raise ValueError

		self.WorkedTimes += 1
		if self.WorkedTimes > WorkStatus.MaxWorkTimes :
			WorkStatus.MaxWorkTimes = self.WorkedTimes
			pass
		self.WaitPOS = self.WorkPOS	# 便于再一次上班的操作
		# 考虑 如何加入多层字典,或加入一个工作次数的信息?
		# 是否需要从等待序列中移除

	def Report():
		print("正在上班的员工信息 : {0}".format(WorkStatus.NormalWorkList), end=' ')
		print("选钟 {0}".format(WorkStatus.SelectedWorkList))

class AllStuff(StuffInfo, WorkStatus):
	"This is the class for AllStuff."

	AllStuffList = []
	DayStuffList = []
	NightStuffList = []

	def __init__(self,StuffNumber, Gender='Male', Shift='Day'):
		StuffInfo.__init__(self, StuffNumber, Gender, Shift)
		WorkStatus.__init__(self)
		AllStuff.AllStuffList.append(self)
		if Shift == 'Day':
			AllStuff.DayStuffList.append(self)
		elif Shift == 'Night':
			AllStuff.NightStuffList.append(self)

	def Wait(self, WaitPOS):
		WorkStatus.Wait(self, WaitPOS)

	def Work(self, WorkType='Normal'):
		WorkStatus.Work(self, WorkType)

WaitList = {}
def MakeWaitList(Time):
	"""12 -- Day, 19 -- All, 24 -- Night.
	
	NOT completed yet.Need more complicated rules.
	"""
	if Time == 12:
		StuffOnDuty = AllStuff.DayStuffList
	elif Time == 19:
		StuffOnDuty = AllStuff.AllStuffList
	elif Time == 24:
		StuffOnDuty = AllStuff.NightStuffList
	
	WaitList.clear()
	WaitPOS = 1
	for Stuff in StuffOnDuty:
		Stuff.Wait(WaitPOS)
		#WaitList[WaitPOS] = Stuff.StuffNumber
		WaitList[WaitPOS] = Stuff
		WaitPOS += 1

if __name__ == '__main__' :
	DayShift_1 = AllStuff(1,'Male','Day')
	DayShift_2 = AllStuff(2,'Male','Day')
	DayShift_3 = AllStuff(3,'Male','Day')
	DayShift_4 = AllStuff(4,'Female','Day')
	NightShift_5 = AllStuff(5,'Female','Night')
	NightShift_6 = AllStuff(6,'Female','Night')
	NightShift_7 = AllStuff(7,'Female','Night')

	time = int(input("请输入上班的时间(12,19,24): "))
	MakeWaitList(time)

	DayShift_1.Work('Normal')
	DayShift_2.Work('Named')
	DayShift_3.Work('Normal')
	DayShift_4.Work('Selected')
	NightShift_5.Work('Normal')
	NightShift_6.Work('Named')
	NightShift_7.Work('Selected')

	WorkStatus.Report()
