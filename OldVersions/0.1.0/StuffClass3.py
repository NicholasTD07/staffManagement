#!/usr/bin/python3
# File Name: StuffClass3.py

from time import time 

import ErrorClass


class StuffInfo :
    "The info of every stuff including StuffNumber, Gender, Shift."

    StuffNumberList = []
    def __init__(self, StuffNumber, Gender, Shift) :
        if StuffNumber in StuffInfo.StuffNumberList :
            print("已有该工号,请检查后重新输入.")
        else :
            self.StuffNumber = StuffNumber
            self.Gender = Gender
            self.Shift = Shift
            StuffInfo.StuffNumberList.append(self.StuffNumber)


class StuffList :
    """ The class contains WorkDict (or WaitList) and POSes."""

    def __init__(self) :
        self.NormalPOS = 0
        self.SelectedPOS = 0
        self.NormalDict = {}  # Use another list to contain StuffList object
        self.SelectedDict = {}  # Two dicts Should be seperated.
        self.WaitDict = {}  # After work done put them here
        

class WorkStatus :

    MaxWorkTimes = 0
    WaitList = StuffList()
    WorkSequence = [WaitList]

    def __init__(self) :
        self.WorkStatus = 'Wait'
        self.WorkedTimes = 0
        self.WorkType = None
        self.WaitPOS = None
        self.WorkPOS = None

    def Wait(self, WaitPOS) :
        # Remove the stuff from WorkDict
        if self.WorkedTimes == 0 :
            pass
        elif (
        self.WorkPOS in self.WorkSequence[self.WorkedTimes].NormalDict 
        ):
            self.WorkSequence[self.WorkedTimes].NormalDict.pop(self.WorkPOS)
        elif (
        self.WorkPOS in self.WorkSequence[self.WorkedTimes].SelectedDict
        ) :
          self.WorkSequence[self.WorkedTimes].SelectedDict.pop(self.WorkPOS)

        self.WaitPOS = WaitPOS
        self.WorkStatus = 'Wait'
        self.WorkType = None
        self.WorkPOS = None
        # Add this stuff to WaitList
        self.WorkSequence[self.WorkedTimes].WaitDict[self.WaitPOS]= self 
        # !!! How to delete from present WorkPOS

    #def PutInSeq(self, Dict, LastPOS, NextPOS) :
    #    NextPOS = LastPOS
    #    self.WorkPOS = NextPOS
    #    NextPOS += 1
    #    Dict[self.WorkPOS] = self
    #    self.WaitPOS = None

    def Work(self, WorkType) :
        if not (
        self in self.WorkSequence[self.WorkedTimes].WaitDict.values()
        ) :
            raise ErrorClass.NotWaiting(
            "工号: {0} 该名员工并不在等待状态.请检查后再输入.".format(self.StuffNumber)
            )
            
        if WorkType == 'Normal' or 'Selected' or 'Named' :
            self.WorkType = WorkType
        else :
            raise ErrorClassWrongType("工作类型有误,请检查后再输入")

        # Remove it from the last WaitDict
        # 在序号没有更新前,将员工从现在的等待序列里移除
        self.WorkSequence[self.WorkedTimes].WaitDict.pop(self.WaitPOS)

        # 更新序号
        self.WorkedTimes += 1
        if self.WorkedTimes > self.MaxWorkTimes : # 若序号大于当前最大值
            WorkStatus.WorkSequence.append(StuffList()) # 则加入一个新的序列
        WorkStatus.MaxWorkTimes = self.WorkedTimes # 加入序列后更新数值,避免重复
        # 此处需要更新类下面的全局变量

        if self.WorkType == 'Normal' :
            self.PutInSeq(
                    WorkStatus.WorkSequence[self.WorkedTimes].NormalDict,
                    WorkStatus.WorkSequence[self.WorkedTimes].NormalPOS,
                    WorkStatus.WorkSequence[self.WorkedTimes].NormalPOS)
        elif self.WorkType == 'Named' :
            if self.WorkSequence[self.WorkedTimes].SelectedDict :
                self.PutInSeq(
                        WorkStatus.WorkSequence[self.WorkedTimes].SelectedDict,
                        WorkStatus.WorkSequence[self.WorkedTimes].SelectedPOS,
                        WorkStatus.WorkSequence[self.WorkedTimes].SelectedPOS)
            else :
                self.PutInSeq(
                        WorkStatus.WorkSequence[self.WorkedTimes].NormalDict,
                        WorkStatus.WorkSequence[self.WorkedTimes].NormalPOS,
                        WorkStatus.WorkSequence[self.WorkedTimes].NormalPOS)
        elif self.WorkType == 'Selected' :
            self.PutInSeq(
                    WorkStatus.WorkSequence[self.WorkedTimes].SelectedDict,
                    self.WaitPOS,
                    WorkStatus.WorkSequence[self.WorkedTimes].SelectedPOS)

    def Report() :
        """显示当前正在工作的员工情况."""

        for WorkList in WorkStatus.WorkSequence :
            #if WorkList.NormalDict and WorkList.SelectedDict :
            if 1 :
                print("第{0}次工作队列 \t".format(
                WorkStatus.WorkSequence.index(WorkList) ))
                print("正常上班序列")
                print("当前上班班号: {0}".format(WorkList.NormalPOS))
                for Stuff in WorkList.NormalDict.values() :
                    print(
                    "员工工号: {0} \t员工上班号码: {1} 员工上班次数: {2}"\
                    .format(
                    Stuff.StuffNumber, Stuff.WorkPOS, Stuff.WorkedTimes) )
                print("选钟后上班序列")
                print("当前上班班号: {0}".format(WorkList.SelectedPOS))
                for Stuff in WorkList.SelectedDict.values() :
                    print(
                    "员工工号: {0} \t员工上班号码: {1} 员工上班次数: {2}"\
                    .format(
                    Stuff.StuffNumber, Stuff.WorkPOS, Stuff.WorkedTimes) )


class AllStuff(StuffInfo, WorkStatus, StuffList) :
    """ This is the class for defining stuffs."""

    AllStuffDict = {}
    DayStuffDict = {}
    NightStuffDict = {}

    def __init__(self, StuffNumber, Gender, Shift) :
        StuffInfo.__init__(self, StuffNumber, Gender, Shift)
        WorkStatus.__init__(self)

        AllStuff.AllStuffDict[self.StuffNumber] = self
        if Shift == 'Day':
            AllStuff.DayStuffDict[self.StuffNumber] = self
        elif Shift == 'Night':
            AllStuff.NightStuffDict[self.StuffNumber] = self
        else :
            raise WrongType("员工性别输入不符合规范")

    def Wait(self, WaitPOS) :
        WorkStatus.Wait(self, WaitPOS)
        # 如果工作次数为0,则送入等待序号
        # 如果工作次数大于零(即工作过,则送入当前工作号)

    def Work(self, WorkType) :
        WorkStatus.Work(self, WorkType)


def MakeWaitList(Time) :
    """12 -- Day, 19 -- All, 24 -- Night.
    
    NOT completed yet.Need more complicated rules.
    """
    if Time == 12:
        StuffOnDuty = AllStuff.DayStuffDict
    elif Time == 19:
        # This part ought to be more complex
        StuffOnDuty = AllStuff.AllStuffDict
    elif Time == 24:
        StuffOnDuty = AllStuff.NightStuffDict
    
    WorkStatus.WorkSequence[0].WaitDict.clear()
    WaitPOS = 1
    for Stuff in StuffOnDuty.values():
        Stuff.Wait(WaitPOS)
        WaitPOS += 1

if __name__ == '__main__' :
    DayShift_1 = AllStuff(1,'Male','Day')
    DayShift_2 = AllStuff(2,'Male','Day')
    DayShift_3 = AllStuff(3,'Male','Day')
    DayShift_4 = AllStuff(4,'Female','Day')
    NightShift_5 = AllStuff(5,'Female','Night')
    NightShift_6 = AllStuff(6,'Female','Night')
    NightShift_7 = AllStuff(7,'Female','Night')

    Time = int(input("请输入上班的时间(12,19,24): "))
    StartTime = time()
    MakeWaitList(Time)

    DayShift_1.Work('Normal')
    DayShift_2.Work('Named')
    DayShift_3.Work('Normal')
    DayShift_4.Work('Selected')
    NightShift_5.Work('Normal')
    NightShift_6.Work('Named')
    NightShift_7.Work('Selected')
    #NightShift_7.Work('Named')
    #NightShift_7.Work('Normal')

    WorkStatus.Report()
    EndTime = time()

    print("整个过程耗时 %.2f" % (EndTime - StartTime))
