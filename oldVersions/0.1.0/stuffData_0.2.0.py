#!/usr/bin/python3
# File Name : stuffData.py


import errorclass


    __version__ = "0.2.0"


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

    Male = 'male'
    Female = 'female'

    def __init__(self, Id, Gender='Male') :
        self.Id = Id
        self.gender = Gender
        self.shift = None
        self.wType = None
        self.wTime = 0 
        self.waitPos = None
        self.workPos = None


class StuffSequence :
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


class StuffContainer :
    """StuffContainer 中含有一组stuff.
    
    StuffContainer 中的 stuff 按照他们的工号(Id)排序.
    Id是不能改变的."""

    FILE_MAGIC_NUMBER = 0x5032D
    FILE_VERSION = 100

    NOR = 'normal'
    NAMED = 'named'
    SEL = 'selected'
    WAIT = 'wait'

    def __init__(self) :
        self.__fileName = ""
        self.__stuffs = {}
        self.__workSeqs = []
        self.__dayShift = {}
        self.__nightShift = {}
        self.__maxSeq = 0
        self.addSeq()
        self.__dirty = False

    def __iter__(self) :
        for stuff in iter(self.__stuffs) :
            yield stuff

    def __len__(self) :
        return len(self.__stuffs)

    def isDirty(self) :
        return self.__dirty

    def setDirty(self, dirty=True) :
        self.__dirty = dirty

    def setFilename(self, fileName) :
        self.__fileName = fileName

    def getFilename(self) :
        return self.__fileName

    def clear(self, cleanFilename=True) :
        self.__stuffs = {}
        self.__workSeqs = []
        self.__dayShift = {}
        self.__nightShift = {}
        self.__maxSeq = 0
        if cleanFilename :
            self.__filename = ""
        self.__dirty = False

    def addSeq(self) :
        """利用最大次数向工作序列中增加员工序列, 加入之前更新__maxSeq"""
        self.__workSeqs.append(StuffSequence())

    def maxSeq(self) :
        """返回工作序列中次数最大的工作序列"""
        return self.__maxSeq

    def setMaxSeq(self, maxSeq) :
        self.__maxSeq = maxSeq

    def updateMaxSeq(self, wTime) :
        """如果员工的工作次数大于当前最大次数,则更新数值.
        
        并且利用addSeq()增加一个序列.
        """
        if wTime > self.maxSeq() :
            self.setMaxSeq(wTime)
            self.addSeq()
            
    def seqByTime(self, wTime) :
        return self.__workSeqs[wTime]

    def thisSeq(self, wTime, seqName) :
        """按照给定的次数以及序列名称返回需要的序列"""
        if seqName is self.NOR :
            return self.seqByTime(wTime).NSeq
        elif seqName is self.SEL :
            return self.seqByTime(wTime).SSeq
        elif seqName is self.WAIT :
            return self.seqByTime(wTime).WSeq

    def addStuff(self, stuff) :
        """如果员工工号不存在,
        
        就将指定的员工(stuff)加入员工列表"""
        if stuff.Id in self.__stuffs :
            return False
        self.__stuffs[stuff.Id] = stuff
        self.__dirty = True
        return True

    def addStuffs(self, *stuffs) :
        """批量添加员工"""
        for stuff in stuffs :
            self.addStuff(stuff)

    def delStuff(self, stuff) :
        """成功删除指定的员工后返回 True.

        如果指定的员工不存在则返回 False.

        TODO :
        从班次队伍中删除成员
        """
        if stuff.Id not in self.__stuffs :
            return False
        del self.__stuffs[stuff.Id]
        self.__dirty = True
        return True

    def stuffId(self, Id) :
        """按照工号(Id)返回员工(stuff)"""
        return self.__stuffs[Id]

    def updateStuff(self, Id, gender, shift) :
        """改变员工信息,可以改变员工性别以及所属班次"""
        stuff = self.stuffId(Id)
        stuff.gender = gender
        stuff.shift = shift
        self.__dirty = True

    def inSeq(self, stuff) :
        if stuff.wType is not None :
            if stuff.wType is self.NOR :
                #return True, self.thisSeq(stuff.wTime, NOR)
                return self.thisSeq(stuff.wTime, self.NOR)
            elif stuff.wType is self.SEL :
                #return True, self.thisSeq(stuff.wTime, SEL)
                return self.thisSeq(stuff.wTime, self.SEL)
        else :
            #return False
            return None
        

    def stuffWait(self, Id) :
        stuff = self.stuffId(Id)
        #ok, Seq = self.inSeq(stuff)
        Seq = self.inSeq(stuff)
        if Seq is not None :
            Seq.pop(stuff.workPos)
            stuff.waitPos = stuff.workPos
        else :
            self.seqByTime(stuff.wTime).WPos += 1
            stuff.waitPos = self.seqByTime(stuff.wTime).WPos
            stuff.workPos = None
        stuff.wType = self.WAIT
        self.thisSeq(stuff.wTime,
            self.WAIT)[stuff.waitPos] = stuff

    def stuffsWait(self, *IDs) :
        """让一队员工进入等待状态"""
        for Id in IDs :
            self.stuffWait(Id)

    def stuffWork(self, Id, wType=NOR) :
        stuff = self.stuffId(Id)
        if stuff.wType is not self.WAIT :
            raise errorclass.notWaiting("员工不在等待状态.")
        self.seqByTime(stuff.wTime).WSeq.pop(stuff.waitPos)
        stuff.wTime += 1
        self.updateMaxSeq(stuff.wTime)
        stuff.wType = wType
        if wType is self.NOR :
            stuff.workPos = self.seqByTime(stuff.wTime).NPos
            self.seqByTime(stuff.wTime).NPos += 1
            self.thisSeq(stuff.wTime,
                self.NOR)[stuff.workPos] = stuff
        elif wType is self.NAMED :
            if seqByTime(stuff.wTime).SSeq :
                self.putInSeq(stuff,
                    self.seqByTime(stuff.wTime).SPos,
                    self.seqByTime(stuff.wTime).SPos,
                    self.seqByTime(stuff.wType).SSeq)
                    #self.thisSeq(stuff.wTime, SEL)
            else :
                self.putInSeq(stuff,
                    self.seqByTime(stuff.wTime).NPos,
                    self.seqByTime(stuff.wTime).NPos,
                    self.seqByTime(stuff.wTime).NSeq)
                #self.thisSeq(stuff.wTime, NOR)
        elif wType is self.SEL :
            self.putInSeq(stuff,
                stuff.waitPos,
                self.seqByTime(stuff.wTime).SPos,
                self.seqByTime(stuff.wTime).SSeq)
                #self.thisSeq(stuff.wTime, SEL)
        return True, "创建员工成功!"

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
                    "员工工号: {0} 上班号码: {1} 上班次数:{2}"\
                    .format(stuff.Id,
                    stuff.workPos, stuff.wTime))
        print("\n END ")
        print("最大工作次数: {0}".format(S.maxSeq()))


if __name__ == '__main__' :
    S = StuffContainer()
    Stuff_1 = Stuff(1)
    Stuff_2 = Stuff(2)
    Stuff_3 = Stuff(3)
    Stuff_4 = Stuff(4)
    Stuff_5 = Stuff(5)
    Stuff_6 = Stuff(6)
    Stuff_7 = Stuff(7)
    Stuff_8 = Stuff(8)
    Stuff_9 = Stuff(9)

    S.addStuffs(Stuff_1, Stuff_2, Stuff_3, Stuff_4, Stuff_5,
        Stuff_6, Stuff_7, Stuff_8, Stuff_9)

    S.stuffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    S.stuffsWork('normal',1, 2, 3, 4, 5, 6, 7, 8, 9)

    S.stuffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    S.stuffsWork('selected', 1, 2, 3, 4, 5, 6, 7, 8, 9)
    S.reportStuffs()
