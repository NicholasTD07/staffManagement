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
        self.SelPOS = 0
        self.NormalDict = {}  # Use another list to contain StuffList object
        self.SelDict = {}  # Two dicts Should be seperated.
        self.WaitDict = {}  # After work done put them here
        

class WorkStatus :

    MaxWorkTimes = 0
    WaitList = StuffList()
    WorkSeq = [WaitList]

    def __init__(self) :
        self.WorkStatus = 'Wait'
        self.WorkTime = 0
        self.WorkType = None
        self.WaitPOS = None
        self.WorkPOS = None

    def Wait(self, WaitPOS) :
        # Remove the stuff from WorkDict
        if self.WorkTime == 0 :
            pass
        elif (
        self.WorkPOS in self.WorkSeq[self.WorkTime].NormalDict 
        ):
            self.WorkSeq[self.WorkTime].NormalDict.pop(self.WorkPOS)
        elif (
        self.WorkPOS in self.WorkSeq[self.WorkTime].SelDict
        ) :
          self.WorkSeq[self.WorkTime].SelDict.pop(self.WorkPOS)

        self.WaitPOS = WaitPOS
        self.WorkStatus = 'Wait'
        self.WorkType = None
        self.WorkPOS = None
        # Add this stuff to WaitList
        self.WorkSeq[self.WorkTime].WaitDict[self.WaitPOS]= self 
        # !!! How to delete from present WorkPOS


    def Work(self, WorkType) :
        if not (
        self in self.WorkSeq[self.WorkTime].WaitDict.values()
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
        self.WorkSeq[self.WorkTime].WaitDict.pop(self.WaitPOS)

        # 更新序号
        self.WorkTime += 1
        if self.WorkTime > self.MaxWorkTimes : # 若序号大于当前最大值
            WorkStatus.WorkSeq.append(StuffList()) # 则加入一个新的序列
        WorkStatus.MaxWorkTimes = self.WorkTime # 加入序列后更新数值,避免重复
        # 此处需要更新类下面的全局变量

        if self.WorkType == 'Normal' :
            # 1 分配当前工作序列号码
            self.WorkPOS = self.WorkSeq[self.WorkTime].NormalPOS
            # 2 自增当前工作序列号码
            self.WorkSeq[self.WorkTime].NormalPOS = (
            self.WorkSeq[self.WorkTime].NormalPOS + 1 )
            # 3 将工作员工放入当前工作序列字典
            self.WorkSeq[self.WorkTime].NormalDict[self.WorkPOS] = self

        elif self.WorkType == 'Named' :
            if self.WorkSeq[self.WorkTime].SelDict : # 有人被选
                # 1
                self.WorkPOS = self.WorkSeq[self.WorkTime].SelPOS
                # 2
                self.WorkSeq[self.WorkTime].SelPOS = (
                self.WorkSeq[self.WorkTime].SelPOS + 1 )
                # 3
                self.WorkSeq[self.WorkTime].SelDict[self.WorkPOS] = self
            else : # SelDict 为空, 没有人被选钟, 放在正常序列
                # 1
                self.WorkPOS = self.WorkSeq[self.WorkTime].NormalPOS
                # 2
                self.WorkSeq[self.WorkTime].NormalPOS = (
                self.WorkSeq[self.WorkTime].NormalPOS + 1 )
                # 3
                self.WorkSeq[self.WorkTime].NormalDict[self.WorkPOS] = self

        elif self.WorkType == 'Selected' :
            # 1
            self.WorkPOS = self.WaitPOS
            # 2
            self.WorkSeq[self.WorkTime].SelPOS = self.WaitPOS + 1
            # 3
            self.WorkSeq[self.WorkTime].SelDict[self.WorkPOS] = self

    def Report() :
        """显示当前正在工作的员工情况."""

        for WorkList in WorkStatus.WorkSeq :
            if WorkList.NormalDict and WorkList.SelDict :
            #if 1 :
                print("第{0}次工作队列 \t".format(
                WorkStatus.WorkSeq.index(WorkList) ))
                print("正常上班序列")
                print("当前上班班号: {0}".format(WorkList.NormalPOS))
                for Stuff in WorkList.NormalDict.values() :
                    print(
                    "员工工号: {0} \t员工上班号码: {1} 员工上班次数: {2}"\
                    .format(
                    Stuff.StuffNumber, Stuff.WorkPOS, Stuff.WorkTime) )
                print("选钟后上班序列")
                print("当前上班班号: {0}".format(WorkList.SelPOS))
                for Stuff in WorkList.SelDict.values() :
                    print(
                    "员工工号: {0} \t员工上班号码: {1} 员工上班次数: {2}"\
                    .format(
                    Stuff.StuffNumber, Stuff.WorkPOS, Stuff.WorkTime) )


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
    
    WorkStatus.WorkSeq[0].WaitDict.clear()
    WaitPOS = 1
    for Stuff in StuffOnDuty.values():
        Stuff.Wait(WaitPOS)
        WaitPOS += 1

if __name__ == '__main__' :
    startTime = time()
    DayShift_1 = AllStuff(1,'Male','Day')
    DayShift_2 = AllStuff(2,'Male','Day')
    DayShift_3 = AllStuff(3,'Male','Day')
    NightShift_5 = AllStuff(5,'Female','Night')
    NightShift_6 = AllStuff(6,'Female','Night')
    NightShift_7 = AllStuff(7,'Female','Night')
    DayShift_4 = AllStuff(4,'Female','Day')
    createTime = time()

    #Time = int(input("请输入上班的时间(12,19,24): "))
    MakeWaitList(19)
    makeListTime = time()

    DayShift_1.Work('Normal')
    NightShift_6.Work('Named')
    DayShift_2.Work('Named')
    NightShift_7.Work('Selected')
    DayShift_3.Work('Normal')
    NightShift_5.Work('Normal')
    DayShift_4.Work('Selected')
    #NightShift_7.Work('Named')
    #NightShift_7.Work('Normal')
    stuffWorkTime = time()

    WorkStatus.Report()
    endTime = time()
    print("""创建员工时间 {0} \n创建列表时间 {1}\n
       
员工工作时间 {2}\n报告时间 {3}"""\
        .format((createTime - startTime),
            (makeListTime - createTime),
            (stuffWorkTime - makeListTime),
            (endTime - stuffWorkTime)))
