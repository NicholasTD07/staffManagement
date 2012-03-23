#!/usr/bin/python3
# File Name : stuffData.py

from time import time

import pickle

from os import path

import errorclass


__version__ = "0.2.4"


class Stuff :
    """Stuff 中包含每个员工的详细信息.
    
    Stuff中包含的信息有, 工号(Id), 性别(Gender),
    工作类型(wType), 工作次数(wTime), 等待位置(waitPos),
    工作位置(workPos),工作序列(workSeq)
    
    工号为整数.
    工作次数,等待位置,工作位置都为整数
    性别可以设置为男('male')或女('female').
    工作类型有正常排钟('normal'),点钟('named')
    ,选钟('selected'),等待('wait').
    工作序列可以为正常(NOR),选钟(SEL),等待(None)

    性别默认为男性,工作类型默认为None,
    加入waitList后为等待(通过Container的wait实现),
    工作次数,等待位置,工作位置,工作序列都默认为None,
    并且通过wait等函数确定.
    """

    MALE = '男'
    FEMALE = '女'

    def __init__(self, Id, Gender=MALE,name=None) :
        self.Id = Id
        self.gender = Gender
        if name is None :
            self.name = ""
        self.shift = None
        self.wType = None
        self.wTime = 0 
        self.waitPos = None
        self.workPos = None


class TimeSequence :
    """员工 工作,等待的序列类.
    
    其中包含了一下信息:
        正常队列的下一个位置(NPos)
        选钟后队列的下一个位置(SPos)
        正常序列(NSeq) -- workPos : Stuff
        选钟序列(SSeq)    同上
        """
    def __init__(self) :
        self.NPos = 1
        self.SPos = 1
        self.WPos = 1
        self.NSeq = {}
        self.SSeq = {}
        self.WSeq = {}
        self.waitPoses = []
        self.workPoses = []

    def __iter__(self) :
        yield 

class StuffContainer :
    """StuffContainer 中含有一组stuff.
    
    StuffContainer 中的 stuff 按照他们的工号(Id)排序.
    Id是不能改变的."""

    FILE_MAGIC_NUMBER = 0x5032D
    FILE_VERSION = 102

    MALE = '男'
    FEMALE = '女'

    NOR = '排钟'
    NAMED = '点钟'
    SEL = '选钟'
    WAIT = '等待'
    IDLE = '休息'

    def __init__(self) :
        self.__fileName = ""
        self.__stuffs = {}
        self.__IDs = []
        self.__workSeqs = []
        self.__modifiedStuffs = []
        self.__maxTime = 0
        self.__largestId = 0
        self.__largestWorkPos = 0
        self.__largestWaitPos = 0
        self.addTimeSeq()
        self.__dirty = False

    #---- 自定义的内置函数 ----#
    def __iter__(self) :
        for stuff in iter(self.__stuffs.values()) :
            yield stuff

    def __len__(self) :
        return len(self.__stuffs)

    #---- 容器本身参数的简单函数 ----#
    def getStuffs(self) :
        return self.__stuffs

    def getIDs(self) :
        return self.__IDs

    def getWorkSeq(self) :
        return self.__workSeqs

    def getLargestId(self) :
        return self.__largestId

    def getLargestWorkPos(self) :
        return self.__largestWorkPos

    def setLargestWorkPos(self, Id) :
        workPos = self.stuffId(Id).workPos
        
        if workPos > self.__largestWorkPos :
            self.__largestWorkPos = workPos

    def getLargestWaitPos(self) :
        return self.__largestWaitPos

    def setLargestWaitPos(self, Id) :
        waitPos = self.stuffId(Id).waitPos
        if waitPos > self.__largestWaitPos :
            self.__largestWaitPos = waitPos

    def isDirty(self) :
        return self.__dirty

    def setDirty(self, dirty=True) :
        self.__dirty = dirty
        print("setDirty({})".format(dirty))

    def getMaxTime(self) :
        """返回工作序列中次数最大的工作序列"""
        return self.__maxTime

    def setMaxTime(self, maxTime) :
        self.__maxTime = maxTime

    def setFilename(self, fileName) :
        self.__fileName = fileName

    def getFilename(self) :
        return self.__fileName

    #---- 容器内容的复杂函数 ----#
    def clear(self, cleanFilename=True) :
        self.__stuffs = {}
        self.__IDs = []
        self.__workSeqs = []
        self.__modifiedStuffs = []
        self.__maxTime = 0
        self.__largestId = 0
        self.__largestWorkPos = 0
        self.__largestWaitPos = 0
        self.addTimeSeq()
        if cleanFilename :
            self.__filename = ""
        self.setDirty(False)

    def getModifiedStuffs(self) :
        return self.__modifiedStuffs

    def modifiedStuff(self, Id) :
        stuff = self.stuffId(Id)
        if stuff in self.__modifiedStuffs :
            print("已有该员工号码")
            return
        self.__modifiedStuffs.append(stuff)
        print("添加改动员工,工号为: {}".format(Id))

    #---- 文件函数 ----#
    @staticmethod
    def fileFormats() :
        return "*.qpc"

    def save(self, fileName="") :
        if fileName :
            self.__fileName = fileName
        if self.__fileName.endswith(".qpc") :
            #print("文件名正确")
            return self.savePickle()
        return False, "保存文件失败: 未知文件格式\n文件: {}"\
                .format(path.basename(self.__fileName))

    def savePickle(self) :
        error = None
        fh = None
        try :
            fh = open(self.__fileName, "wb")
            pickle.dump(self, fh)
        except EnvironmentError as e :
            error = "保存失败: {}".format(e)
        finally :
            if fh is not None :
                fh.close()
            if error is not None :
                return False, error
            self.__dirty = False
            return True, "保存成功!\n已在文件: {0} 中保存数据"\
                .format(path.basename(self.__fileName))

    def load(self, fileName="") :
        if fileName :
            self.__fileName = fileName
        if self.__fileName.endswith(".qpc") :
            #print("文件名正确")
            return self.loadPickle()
        return False, "读取文件失败: 未知文件格式\n文件: {}"\
                .format(path.basename(self.__fileName))
        
    def loadPickle(self) :
        error = None
        fh = None
        stuffs = None
        try :
            fh = open(self.__fileName, "rb")
            self.clear(False)
            stuffs = pickle.load(fh)
        except EnvironmentError as e :
            error = "读取失败: {}".format(e)
        finally :
            if fh is not None :
                fh.close()
            if error is not None :
                return False, error
            self.__dirty = False
            return (True,"读取成功!\n已从文件 :{} 中读取数据"\
                .format(path.basename(self.__fileName)),
                    stuffs)

        


    #---- 有关时间(次数)队列的函数 ----#
    def addTimeSeq(self) :
        """利用最大次数向工作序列中增加员工序列, 加入之前更新__maxTime"""
        self.__workSeqs.append(TimeSequence())

    def updateMaxSeq(self, Id) :
        """如果员工的工作次数大于当前最大次数,则更新数值.
        
        并且利用addTimeSeq()增加一个序列.
        """
        wTime = self.getWorkTime(Id)
        if wTime > self.__maxTime :
            self.__maxTime = wTime
            print("更新最大次数: {}".format(wTime))
            while len(self.__workSeqs) < (wTime + 1) :
                self.addTimeSeq()
                print("添加序列")

    def updateMaxSeqByTime(self, wTime) :
        """如果员工的工作次数大于当前最大次数,则更新数值.
        
        并且利用addTimeSeq()增加一个序列.
        """
        if wTime > self.__maxTime :
            self.__maxTime = wTime
            print("更新最大次数: {}".format(wTime))
            while len(self.__workSeqs) < (wTime + 1) :
                self.addTimeSeq()
                print("添加序列")
            
        #---- 时间队列的简单函数 ----#
        #!-- 注意:利用以下函数时需要根据上下文严格控制当前工作次数 --!#
    def getTimeSeq(self, Id) :
        return self.__workSeqs[self.getWorkTime(Id)]

    def getNSeq(self, Id) :
        return self.getTimeSeq(Id).NSeq

    def getSSeq(self, Id) :
        return self.getTimeSeq(Id).SSeq

    def getWSeq(self, Id) :
        return self.getTimeSeq(Id).WSeq

    def getNPos(self, Id) :
        return self.getTimeSeq(Id).NPos

    def getSPos(self, Id) :
        return self.getTimeSeq(Id).SPos

    def getWPos(self, Id) :
        return self.getTimeSeq(Id).WPos

    def setNPos(self, Id, NPos) :
        self.getTimeSeq(Id).NPos = NPos

    def setSPos(self, Id, SPos) :
        self.getTimeSeq(Id).SPos = SPos

    def setWPos(self, Id, WPos) :
        self.getTimeSeq(Id).WPos = WPos

    def incNPos(self, Id) :
        self.setNPos(Id, (self.getNPos(Id) + 1)) 

    def incSPos(self, Id) :
        self.setSPos(Id, (self.getSPos(Id) + 1)) 

    def incWPos(self, Id) :
        self.setWPos(Id, (self.getWPos(Id) + 1)) 

    def putInNSeq(self, Id) :
        self.getNSeq(Id)[self.getWorkPos(Id)] = self.stuffId(Id)

    def putInSSeq(self, Id) :
        self.getSSeq(Id)[self.getWorkPos(Id)] = self.stuffId(Id)

    def putInWSeq(self, Id) :
        self.getWSeq(Id)[self.getWaitPos(Id)] = self.stuffId(Id)

    def popFromNSeq(self, Id) :
        self.getNSeq(Id).pop(self.getWorkPos(Id))

    def popFromSSeq(self, Id) :
        self.getSSeq(Id).pop(self.getWorkPos(Id))

    def popFromWSeq(self, Id) :
        self.getWSeq(Id).pop(self.getWaitPos(Id))

    def getWaitPoses(self, Id) :
        return self.getTimeSeq(Id).waitPoses

    def getWorkPoses(self, Id) :
        return self.getTimeSeq(Id).workPoses

    def addWaitPoses(self, Id) :
        #print("添加等待序号")
        self.getWaitPoses(Id).append((self.getWaitPos(Id),Id))
        #print("此列等待序号: {}".format(self.getWaitPoses(Id)))

    def popWaitPoses(self, Id) :
        #print("poping waitPos: {}".format(Id))
        self.getWaitPoses(Id).remove((self.getWaitPos(Id),Id))
        #print("当前等待序列: {}".format(self.getWaitPoses(Id)))

    def addWorkPoses(self, Id) :
        #print("添加工作序号")
        self.getWorkPoses(Id).append((self.getWorkPos(Id),Id))
        #print("此列工作序号: {}".format(self.getWorkPoses(Id)))

    def popWorkPoses(self, Id) :
        #print("poping workPos: {}".format(Id))
        self.getWorkPoses(Id).remove((self.getWorkPos(Id),Id))

        #---- 利用以上简单函数构成的复杂函数 ----#
    def waitPosAvaliable(self, wTime, waitPos) :
        #print("检查等待序号")
        if waitPos not in self.__workSeqs[wTime].waitPoses :
            return True
        else :
            return False

    def workPosAvaliable(self, wTime, workPos) :
        #print("检查工作序号\n wTime: {0} workPos: {1}"\
        #        .format(wTime, workPos))
        if workPos in self.__workSeqs[wTime].workPoses :
            #print("工作序号存在")
            return False
        else :
            #print("工作序号不存在")
            return True

    def popFromWorkSeq(self, Id) :
        wType = self.getWorkType(Id)
        if wType is self.NOR :
            self.popFromNSeq(Id)
        elif wType is self.SEL :
            self.popFromSSeq(Id)

    #---- 与员工有关的函数 ----#

        #---- 员工的基本函数 ----#
    def updateStuff(self, Id,
        gender=None, name=None, shift=None) :
        if Id not in self.__stuffs : # 没有员工工号, 添加员工
            self.__stuffs[Id] = Stuff(Id)
            self.__IDs.append(Id)
            self.__IDs.sort()
            if Id > self.__largestId :
                self.__largestId = Id
            self.setWorkType(Id, self.IDLE)
        if gender is not None :
            self.stuffId(Id).gender = gender
        if name is not None :
            self.stuffId(Id).name = name
        if shift is not None :
            self.stuffId(Id).shift = shift
        self.setDirty()

    def addStuffs(self, gender, *IDs) :
        for Id in IDs :
            self.updateStuff(Id,gender)

    def deleteStuff(self, Id) :
        """成功删除指定的员工后返回 True.

        如果指定的员工不存在则返回 False.

        TODO :
        从班次队伍中删除成员
        """
        if Id not in self.__stuffs :
            return False
        if self.inWorkSeq(Id) is not None :
            self.popWorkPoses(Id)
            self.popFromWorkSeq(Id)
        else :
            self.popWaitPoses(Id)
            self.popFromWSeq(Id)
        self.__IDs.remove(Id)
        del self.__stuffs[Id]
        self.setDirty()
        return True

    def stuffId(self, Id) :
        """按照工号(Id)返回员工(stuff)"""
        if Id in self.__stuffs :
            return self.__stuffs[Id]
        else :
            return False

        #---- 员工信息的简单函数 ----#
    def getWorkTime(self, Id) :
        return self.stuffId(Id).wTime

    def setWorkTime(self, Id, wTime) :
        self.stuffId(Id).wTime = wTime

    def incWorkTime(self, Id) :
        self.setWorkTime(Id, (self.getWorkTime(Id) + 1))

    def getWorkType(self, Id) :
        return self.stuffId(Id).wType

    def setWorkType(self, Id, wType) :
        self.stuffId(Id).wType = wType

    def getWaitPos(self, Id) :
        return self.stuffId(Id).waitPos

    def setWaitPos(self, Id, waitPos) :
        self.stuffId(Id).waitPos = waitPos
        self.modifiedStuff(Id)

    def getWorkPos(self, Id) :
        return self.stuffId(Id).workPos

    def setWorkPos(self, Id, workPos) :
        self.stuffId(Id).workPos = workPos
        self.modifiedStuff(Id)

        #---- 员工的复杂函数 ----#
    def updateWorkStatus(self, Id, wTime=None, wType=None,
        waitPos=None, workPos=None) :
        """用来更新员工的工作状态.调用时写入参数关键字"""
        if Id not in self.__stuffs :
            raise noThisStuff("没有此名员工工号")
        if wTime is not None :
            self.stuffId(Id).wTime = wTime
        if wType is not None :
            self.stuffId(Id).wType = wType
        if waitPos is not None :
            self.stuffId(Id).waitPos = waitPos
            self.setLargestWaitPos(Id)
        if workPos is not None :
            self.stuffId(Id).workPos = workPos
            self.setLargestWorkPos(Id)
        self.modifiedStuff(Id)
        self.setDirty()

    def inWorkSeq(self, Id) :
        wType = self.getWorkType(Id)
        wTime = self.getWorkTime(Id)
        if wType is self.NOR :
            return self.getNSeq(Id)
        elif wType is self.SEL :
            return self.getSSeq(Id)
        else :
            return None
        
    def stuffWait(self, Id) :
        if self.inWorkSeq(Id) is not None :
            self.popWorkPoses(Id)
            self.popFromWorkSeq(Id)
            self.setWaitPos(Id, self.getWorkPos(Id))
        else :
            self.setWaitPos(Id, self.getWPos(Id))
            self.incWPos(Id)
        waitPos = self.getWaitPos(Id)
        if waitPos > self.__largestWaitPos :
            self.__largestWaitPos = waitPos
        self.setWorkPos(Id, None)
        #self.stuffId(Id).workPos = None
        self.setWorkType(Id, self.WAIT)
        #self.stuffId(Id).wType = self.WAIT
        self.addWaitPoses(Id)
        self.putInWSeq(Id)
        self.modifiedStuff(Id)


    def stuffsWait(self, *IDs) :
        """让一队员工进入等待状态"""
        for Id in IDs :
            self.stuffWait(Id)

    def goWork(self, Id) :
        wType = self.getWorkType(Id)
        if wType is self.NOR :
            self.setWorkPos(Id, self.getNPos(Id))
            self.putInNSeq(Id)
            self.incNPos(Id)
        elif wType is self.SEL :
            self.setWorkPos(Id, self.getWaitPos(Id))
            self.putInSSeq(Id)
            self.setSPos(Id, (self.getWaitPos(Id) + 1))
        elif wType is self.NAMED :
            if self.getSSeq(Id) :
                self.setWorkPos(Id, self.getSPos(Id))
                self.putInSSeq(Id)
                self.incSPos(Id)
            else :
                self.setWorkPos(Id, self.getNPos(Id))
                self.putInNSeq(Id)
                self.incNPos(Id)
        else :
            raise (
                errorclass.wrongType(
                    "类型不对.\t 当前类型为: {}".format(wType)))
        
    def stuffWork(self, Id, wType=NOR) :
        if self.getWorkType(Id) is not self.WAIT :
            raise errorclass.notWaiting("员工不在等待状态.")
        self.popWaitPoses(Id)
        self.popFromWSeq(Id)
        self.incWorkTime(Id)
        self.updateMaxSeq(Id)
        self.setWorkType(Id, wType)
        #self.stuffId(Id).wType = wType
        self.goWork(Id)
        workPos = self.getWorkPos(Id)
        if workPos > self.__largestWorkPos :
            self.__largestWorkPos = workPos
        self.setWaitPos(Id, None)
        #self.stuffId(Id).waitPos = None
        self.addWorkPoses(Id)
        self.modifiedStuff(Id)

    def stuffsWork(self, wType=NOR, *IDs) :
        """员工批量工作"""
        for Id in IDs:
            self.stuffWork(Id, wType)

    def reportStuffs(self) :
        """汇报当前正在工作的员工情况."""
        print("含有{0}名员工.".format(len(S)))
        for workSeq in self.__workSeqs :
            if 1 :
                print("第{0}次工作队列 \t"\
                    .format(self.__workSeqs.index(workSeq)))
                print()
                print("正常上班序列")
                print("当前上班班号: {0}"\
                    .format(workSeq.NPos))
                for stuff in workSeq.NSeq.values() :
                    print(
                    "员工工号: {0} 上班号码: {1} 上班次数:{2}"\
                    .format(stuff.Id,
                    stuff.workPos, stuff.wTime))
                print()
                print("选钟后上班序列")
                print("当前上班班号: {0}"\
                    .format(workSeq.SPos))
                for stuff in workSeq.SSeq.values() :
                    print(
                    "员工工号: {0} 上班号码: {1} 上班次数:{2}"\
                    .format(stuff.Id,
                    stuff.workPos, stuff.wTime))
                print()
                print("等待员工")
                print("当前等待班号: {0}"\
                    .format(workSeq.WPos))
                for stuff in workSeq.WSeq.values() :
                    print(
                    "员工工号: {0} 等待号码: {1} 上班次数:{2}"\
                    .format(stuff.Id,
                    stuff.waitPos, stuff.wTime))
        print("\n END ")
        print("最大工作次数: {0}".format(S.getMaxTime()))

    def tell(self, Id) :
        print("工号: {}\t姓名: {}\t性别: {}\t工作位置: {}, 等待位置: {}"\
            .format(self.stuffId(Id).Id,self.stuffId(Id).name,
                self.stuffId(Id).gender, self.stuffId(Id).workPos,
                self.stuffId(Id).waitPos))


if __name__ == '__main__' :
    S = StuffContainer()

    startTime = time()
    S.addStuffs(S.MALE, 1,2,3,4,5,6,7,8,9)
    createTime = time()
    S.stuffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    S.reportStuffs()
    #S.stuffsWork(S.NOR,1, 2, 3, 4, 5, 6, 7, 8, 9)
    #stuffWorkTime = time()

    #S.stuffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    #S.stuffsWork(S.SEL, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    #S.stuffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    #stuffWork2Time = time()
    #S.reportStuffs()
    #endTime = time()
#    print("""创建员工时间 {0} \n
#员工第一次工作时间 {1}\n员工第二次工作时间 {2}
#报告时间 {3}"""\
#        .format((createTime - startTime),
#            (stuffWorkTime - createTime),
#            (stuffWork2Time - stuffWorkTime),
#            (endTime - stuffWorkTime)))
#    print("员工工号: {}".format(S.getIDs()))


    S.save("/home/thedevil/test.qpc")
    S.load("/home/thedevil/test.qpc")
