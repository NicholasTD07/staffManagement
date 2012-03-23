#!/usr/bin/python3
# File Name : stuffData.py

from os import path
import pickle
import errorclass


__version__ = "0.3.0"


DEBUG = True


class Stuff :
    """包含员工的详细信息"""

    def __init__(self, Id, gender=StuffContainer.MALE, name=None) :
        self.Id = Id
        self.gender = gender
        if name is not None :
            self.name = name
        else :
            self.name = ""
        self.waitPos = None
        self.workPos = None
        self.wTime = 0
        self.wType = self.IDLE
        self.sType = None


class TimeSeq :
    """包含不同工作次数的员工"""

    def __init__(self) :
        self.nPos = 1
        self.sPos = 1
        self.wPos = 1
        self.nSeq = {}
        self.sSeq = {}
        self.wSeq = {}
        self.waitPoses = []
        self.workPoses = []


class StuffContainer :
    """员工以及工作对列的容器"""

    MALE = '男'
    FEMALE = '女'

    NOR = '排钟'
    NAMED = '点钟'
    SEL = '选钟'
    WAIT = '等待'
    IDLE = '休息'

    def __init__(self) :
        self.__IDs = []
        self.__stuffs = {}
        self.__modStuffs = []
        self.__workSeqs = []
        self.__maxTime = 0
        self.__maxId = 0
        self.__maxWorkPos = 0
        self.__maxWaitPos = 0
        self.__fileName = ""
        self.__dirty = False
        self.addTimeSeq()

    #---- 自定义内置函数 ----#

    def __iter__(self) :
        for stuff in iter(self.__stuffs.values()) :
            yield stuff

    def __len__(self) :
        return len(self.__stuffs)

    #------------------------#

    #---- 容器的简单函数 ----#

    #-- 返回及设置属性 --#

    def getIDs(self) :
        return self.__IDs

    def getStuffs(self) :
        return self.__stuffs

    def getModStuffs(self) :
        return self.__modStuffs

    def getWorkSeq(self) :
        return self.__workSeqs

    def getMaxTime(self) :
        return self.__maxTime

    def updateMaxTime(self, time) :
        self.log("\n更新最大工作次数:\t")
        if time > self.__maxTime :
            self.__maxTime = time
            self.log("更新为: {}!".format(time))
        else :
            self.log("保持不变: {}.".format(self.__maxTime))

    def getMaxId(self) :
        return self.__maxId

    def updateMaxId(self, Id) :
        self.log("\n更新最大工号:\t")
        if Id > self.__maxId :
            self.__maxId = Id
            self.log("更新为: {}!".format(Id))
        else :
            self.log("保持不变: {}.".format(self.__maxId))

    def getMaxWorkPos(self) :
        return self.__maxWorkPos

    def updateMaxWorkPos(self, workPos) :
        self.log("\n更新最大工作位置: \t")
        if workPos > self.__maxWorkPos :
            self.__maxWorkPos = workPos
            self.log("更新为: {}!".format(waitPos))
        else :
            self.log("保持不变: {}.".format(self.__maxWaitPos))

    def getMaxWaitPos(self) :
        return self.__maxWaitPos

    def updateMaxWaitPos(self, waitPos) :
        self.log("\n更新最大等待位置: \t")
        if waitPos > self.__maxWaitPos :
            self.__maxWaitPos = waitPos
            self.log("更新为: {}!".format(waitPos))
        else :
            self.log("保持不变: {}.".format(self.__maxWaitPos))

    def getFileName(self) :
        return self.__fileName

    def setFileName(self, fileName) :
        self.__fileName = fileName

    def isDirty(self) :
        return self.__dirty

    def setDirty(self, dirty=True) :
        self.__dirty = dirty
        self.log("\n设置改动(__dirty): {}.".format(dirty))

    #--------------------#

    #---- 文件操作 ----#

    def log(self, msg) :
        if DEBUG :
            logstr = "".format(msg)
            print(logstr)
            logfile = "./log.txt"
            try :
                log = open(logfile, "w")
                log.write(logstr)
            except EnvironmentError as e :
                error = "记录失败! {}".format(e)
                print(error)
            finally :
                log.close()

    @staticmethod
    def fileFormats() :
        return "*.qpc"

    def save(self, fileName="") :
        if fileName :
            self.__fileName = fileName
        if self.__fileName.endswith(".qpc") :
            self.log("\n保存文件: 文件后缀正确!")
            return self.savePickle()
        msg = "\n保存文件: 文件后缀错误."
        self.log(msg)
        return False, msg 

    def savePickle(self)
        error = None
        theFile = None
        try :
            theFile = open(self.__fileName, "wb")
            pickle.dump(self, fh)
        except EnvironmentError as e :
            error = "\n保存文件: 失败. 错误: {}".format(e)
            self.log(error)
        finally :
            if theFile is not None :
                theFile.close()
            if error is not None :
                return False, error
            msg = "\n保存文件: 成功!"
            self.log(msg)
            return True, msg

    def load(self, fileName="") :
        if fileName ;
            self.__fileName = fileName
        if self.__fileName.endswith(".qpc") :
            self.log("\n读取文件: 文件后缀正确!")
            return self.loadPickle()
        msg = "\n读取文件: 文件后缀错误."
        self.log(msg)
        return False, msg

    def loadPickle(self) :
        error = None
        theFile = None
        try :
            theFile = open(self.__fileName, "rb")
            self.clear(False)
            stuffs = pickle.load(theFile)
        except EnvironmentError as e :
            error = "\n读取文件: 失败. 错误: {}".format(e)
            self.log(error)
        finally :
            if theFile is not None :
                theFile.close()
            if error is not None :
                return False, error
            self.dirty = False
            msg = "\n读取文件: 成功!"
            self.log(msg)
            return True, msg, stuffs

    #------------------#

    #---- 时间队列 ----#

    #-- 操纵容器内时间队列 --#

    def addTimeSeq(self) :
        self.__workSeqs.append(TimeSeq())
        self.log("\n添加时间队列.")

    def updateMaxSeq(self, time) :
        if time > self.__maxTime :
            self.__maxTime = time
            self.log("\n更新时间队列: 自动更新最大工作次数.")
            count = 0
        while len(self.__workSeqs) < ( time + 1 ) :
            self.__workSeqs.append(TimeSeq())
            count += 1
        self.log("\n更新时间队列: 自动增加了{}列时间队列"\
                        .format(count))

    #-- 返回及设置属性 --#

    # 返回队列 #

    def getTimeSeq(self, time) ;
        return self.__workSeqs[time]

    def getNSeq(self, time) :
        return self.__workSeqs[time].nSeq

    def getSSeq(self, time) :
        return self.__workSeqs[time].sSeq

    def getWSeq(self, time) :
        return self.__workSeqs[time].wSeq

    # 返回及设置位置 #

    def getNPos(self, time) :
        return self.__workSeqs[time].nPos

    def getSPos(self, time) :
        return self.__workSeqs[time].sPos

    def getWPos(self, time) :
        return self.__workSeqs[time].wPos

    def setNPos(self, time, nPos) :
        self.__workSeqs[time].nPos = nPos

    def setSPos(self, time, sPos) :
        self.__workSeqs[time].sPos = sPos

    def setWPos(self, time, wPos) :
        self.__workSeqs[time].wPos = wPos

    def incNPos(self, time) :
        self.__workSeqs[time].nPos += 1

    def incSPos(self, time) :
        self.__workSeqs[time].sPos += 1

    def incWPos(self, time) :
        self.__workSeqs[time].wPos += 1

    def putInSeq(self, Id) :
        stuff = self.__stuffs[Id]
        time = stuff.time
        sType = stuff.sType
        self.log("\n员工入队: 工号:{}, 工作次数:{}"
                .format(Id, time))
        self.log("\n\t 员工入队类型: {}".format(sType))
        if sType is self.NOR : 
            workPos = stuff.workPos
            self.log("入队位置: {}".format(workPos))
            self.__workSeqs[time].nSeq[workPos]= stuff
        elif sType is self.SEL: 
            workPos = stuff.workPos
            self.log("入队位置: {}".format(workPos))
            self.__workSeqs[time].sSeq[workPos]= stuff
        elif sType is self.WAIT :
            waitPos = stuff.waitPos
            self.log("入队位置: {}".format(waitPos))
            self.__workSeqs[time].wSeq[waitPos]= stuff
        else :
            msg = "\n员工入队: 错误工作类型."
            self.log(msg)
            raise errorclass.wrongType(msg)

    def popFromSeq(self, Id) :
        stuff = self.__stuffs[Id]
        time = stuff.time
        sType = stuff.sType
        self.log("\n员工出队: 工号:{}, 工作次数:{}"
                .format(Id, time))
        self.log("\n\t 员工出队类型: {}".format(sType))
        if sType is self.NOR :
            workPos = stuff.workPos
            self.log("出队位置: {}".format(workPos))
            self.__workSeqs[time].nSeq.pop(workPos)
        elif sType is self.SEL :
            workPos = stuff.workPos
            self.log("出队位置: {}".format(workPos))
            self.__workSeqs[time].sSeq.pop(workPos)
        elif sType is self.WAIT :
            waitPos = stuff.waitPos
            self.log("出队位置: {}".format(waitPos))
            self.__workSeqs[time].wSeq.pop(waitPos)
        else :
            msg = "\n员工出队: 错误工作类型."
            self.log(msg)
            raise errorclass.wrongType(msg)
            
    def getWorkPoses(self, time) :
        return self.__workSeqs[time].workPoses

    def addWorkPoses(self, Id) :
        stuff = self.__stuffs[Id]
        time = stuff.time
        workPos = stuff.workPos
        self.__workSeqs[time].workPoses.append( (workPos, Id) )
        self.log("\n向第{}次时间队列 添加:员工工作位置:{}及工号:{}"\
                .format(time, workPos, Id))

    def popWorkPoses(self, Id) :
        stuff = self.__stuffs[Id]
        time = stuff.time
        workPos = stuff.workPos
        self.__workSeqs[time].workPoses.remove( (workPos, Id) )
        self.log("\n从第{}次时间队列 去除:员工工作位置:{}及工号:{}"\
                .format(time, workPos, Id))
        
    def getWaitPoses(self, time) :
        return self.__workSeqs[time].waitPoses

    def addWaitPoses(self, Id) :
        stuff = self.__stuffs[Id]
        time = stuff.time
        waitPos = stuff.waitPos
        self.__workSeqs[time].waitPoses.append( (waitPos, Id) )
        self.log("\n向第{}次时间队列 添加:员工等待位置:{}及工号:{}"\
                .format(time, waitPos, Id))

    def popWaitPoses(self, Id) :
        stuff = self.__stuffs[Id]
        time = stuff.time
        waitPos = stuff.waitPos
        self.__workSeqs[time].waitPoses.remove( (waitPos, Id) )
        self.log("\n从第{}次时间队列 去除:员工等待位置:{}及工号:{}"\
                .format(time, waitPos, Id))

    # 检查工作位置以及等待位置 #

    def checkWorkPos(self, time, workPos) :
        self.log("\n检查第{}次时间队列内是否含有{}工作位置."\
            .format(time, workPos))
        if workPos not in self.__workSeqs[time].workPoses :
            self.log("\t 没有该工作位置, 可以使用!")
            return True
        else :
            self.log("\t 已有该工作位置, 不能使用!")
            return False

    def checkWaitPos(self, time, waitPos) :
        self.log("\n检查第{}次时间队列内是否含有{}等待位置."\
            .format(time, waitPos))
        if waitPos not in self.__workSeqs[time].waitPoses :
            self.log("\t 没有该等待位置, 可以使用!")
            return True
        else :
            self.log("\t 已有该等待位置, 不能使用.")
            return False
        

    #---- 员工信息 ----#

    #-- 员工基本函数(创建,更新,删除) --#

    def updateStuff(self, Id, gender=None, name=None) :
        if Id not in self.__stuffs :
            self.__stuffs[Id] = Stuff(Id)
            self.__IDs.append(Id)
            self.__IDs.sort()
            if Id > self.__maxId :
                self.__maxId = Id
            self.stuffs[Id].wType = self.IDLE
        if gender is not None :
            self.stuffs[Id].gender = gender
        if name is not None :
            self.stuffs[Id].name = name
        if stuff not in self.__modStuffs :
            self.__modStuffs.append(self.__stuffs[Id])
        self.__dirty = True

    def updateWorkStatus(self, Id, wTime=None, wType=-1,
                waitPos=-1, workPos=-1) :
        if Id not in self.__stuffs :
            raise noThisStuff("没有此名员工工号")
        if wTime is not -1 :
            self.__stuffs[Id].wTime = wTime
        if wType is not -1 :
            self.__stuffs[Id].wType = wType
        if waitPos is not -1 :
            self.__stuffs[Id].waitPos = waitPos
            if waitPos > self.__maxWaitPos :
                self.__maxWaitPos = waitPos
        if workPos is not -1 :
            self.__stuffs[Id].workPos = workPos
            if workPos > self.__maxWorkPos :
                self.__maxWorkPos = workPos
        if stuff not in self.__modStuffs :
            self.__modStuffs.append(self.__stuffs[Id])
        self.__dirty = True

    def addStuffs(self, gender, *IDs) :
        for Id in IDs :
            self.updateStuff(Id, gender)

    def deleteStuff(self, Id) :
        if Id not in self.__stuffs :
            return
        stuff = self.__stuffs[Id]
        time = stuff.time
        wType = stuff.wType
        sType = stuff.sType
        # 员工信息可能存在的位置:
        #   1.self.__stuffs 2.self.__IDs
        #   3.self.__workSeqs 某个时间队列中 a.工作\等待队列
        #       b.工作\等待位置队列中

        # 1.从位置序列中移除
        if wType is self.WAIT :
            waitPos = stuff.waitPos
            self.__workSeqs[time].waitPoses.remove( (waitPos, Id) )
            self.log("\n从第{}次时间队列去除:员工等待位置:{}及工号:{}"\
                .format(time, waitPos, Id))
        elif wType is self.IDLE :
            pass
        else :
            workPos = stuff.workPos
            self.__workSeqs[time].workPoses.remove( (workPos, Id) )
            self.log("\n从第{}次时间队列去除:员工工作位置:{}及工号:{}"\
                .format(time, workPos, Id))
        # 2.从时间队列的工作等待队列中移除
        if sType is self.NOR :
            self.log("出队位置: {}".format(workPos))
            self.__workSeqs[time].nSeq.pop(workPos)
        elif sType is self.SEL :
            self.log("出队位置: {}".format(workPos))
            self.__workSeqs[time].sSeq.pop(workPos)
        elif sType is self.WAIT :
            self.log("出队位置: {}".format(waitPos))
            self.__workSeqs[time].wSeq.pop(waitPos)
        # 3.从self.__IDs 中移除
        self.__IDs.remove(Id)
        # 4.删除员工信息
        del self.__stuffs[Id]
        if Id not in self.__modStuffs :
            self.__modStuffs.append(Id)
        self.__dirty = True

    #-- 员工工作等待函数 --#

    def stuffWait(self, Id) :
        if Id not in self.__stuffs :
            return
        self.log("\n{} 员工进入等待序列: ".format(Id))
        stuff = self.__stuffs[Id]
        time = stuff.time
        wType = stuff.wType
        sType = stuff.sType

        # 1.从当前时间队列位置序列中移除
        # 1.plus 利用当前信息, 设置waitPos, 处理当前时间队列的wPos
        if wType is self.WAIT :
            self.log("\n已在等待序列中,无处理.")
        elif wType is self.IDLE :
            # 员工创建后第一次进入等待状态
            wPos = self.__workSeqs[time].wPos
            stuff.waitPos = wPos
            self.__workSeqs[time].wPos += 1
            self.log(
            "员工获得等待序号: {}.第{}次时间队列新的等待序号为: {}"\
            .format(stuff.waitPos, self.__workSeqs[time].wPos))
        else : # 员工处于任何一种工作状态
            workPos = stuff.workPos
            self.__workSeqs[time].workPoses.remove( (workPos, Id) )
            self.log("\n从第{}次时间队列去除:员工工作位置:{}及工号:{}"\
                .format(time, workPos, Id))
            stuff.waitPos = workPos
            self.__workSeqs[time].wPos = workPos + 1
            self.log(
            "员工获得等待序号: {}.第{}次时间队列新的等待序号为: {}"\
            .format(stuff.waitPos, self.__workSeqs[time].wPos))

        # 2.从当前时间队列的工作等待队列中移除
        if sType is self.NOR :
            self.log("出队位置: {}".format(workPos))
            self.__workSeqs[time].nSeq.pop(workPos)
        elif sType is self.SEL :
            self.log("出队位置: {}".format(workPos))
            self.__workSeqs[time].sSeq.pop(workPos)
        elif sType is self.WAIT :
            self.log("已在等待序列中,不执行出队操作.")
        else :
            self.log("不存在任何工作等待队列中.无出队操作.")

        # 3. 添加该等待位置, 并且将员工放入当前时间队列的等待序列
        self.__workSeqs[time].waitPoses.append( (waitPos, Id) )
        self.__workSeqs[time].wSeq[waitPos] = stuff

        # 4. 检查当前waitPos是否为最大,更新maxWaitPos
        waitPos = stuff.waitPos
        if waitPos > self.__maxWaitPos :
            self.__maxWaitPos = waitPos

        # 5. 清除工作位置, 改变工作类型
        stuff.workPos = None
        stuff.wType = self.WAIT
        stuff.sType = self.WAIT

        # 6. 添加为修改过的员工, 并且记录事件
        self.__modStuffs.append(stuff)
        self.log(
            "\n{}员工等待操作完成!\t第{}次时间队列\t等待位置{}\t"\
            .format(Id, time, waitPos))

    def stuffWork(self, Id, wType=NOR) :
        if Id not in self.__stuffs :
            return
        self.log("\n{} 员工进入工作序列: ".format(Id))
        stuff = self.__stuffs[Id]
        time = stuff.time
        if stuff.wType is not self.WAIT :
            msg = "员工不在等待状态."
            self.log(msg)
            raise errorclass.notWaiting(msg)

        # 1.从等待序列以及等待位置序列中弹出
        waitPos = stuff.waitPos
        self.__workSeqs[time].waitPoses.remove( (waitPos, Id) )
        self.log("\n从第{}次时间队列去除:员工等待位置:{}及工号:{}"\
            .format(time, waitPos, Id))
        self.__workSeqs[time].wSeq.pop(waitPos)
        self.log("{}员工从等待序列出队,位置: {}".format(Id, waitPos))

        # 2.增加工作次数, 并检查是否为最大次数且是否需要更新时间队列
        stuff.wTime += 1
        time = stuff.wTime
        if time > self.__maxTime :
            self.__maxTime = time
            self.log("\n更新时间队列: 自动更新最大工作次数.")
            count = 0
        while len(self.__workSeqs) < ( time + 1 ) :
            self.__workSeqs.append(TimeSeq())
            count += 1
        self.log("更新时间队列: 自动增加了{}列时间队列".format(count))

        # 3.设置工作类型
        stuff.wType = wType

        # 4. goWork...
        time = stuff.wTime
        if wType is self.NOR :
            nPos = self.__workSeqs[time].nPos
            stuff.workPos = nPos
            self.__workSeqs[time].nSeq[stuff.workPos] = stuff
            self.__workSeqs[time].nPos += 1
            # 由于增加了 sType 所以需要在工作时设置它的内容
            stuff.sType = self.NOR
        elif wType is self.SEL :
            waitPos = stuff.waitPos
            stuff.workPos = waitPos
            self.__workSeqs[time].sSeq[stuff.workPos] = stuff
            self.__workSeqs[time].sPos = waitPos + 1
            stuff.sType = self.SEL
        elif wType is self.NAMED :
            if self.__workSeqs[time].sSeq :
                sPos = self.__workSeqs[time].sPos
                stuff.workPos = sPos
                self.__workSeqs[time].sSeq[stuff.workPos] = stuff
                self.__workSeqs[time].sPos += 1
                stuff.sType = self.SEL
            else :
                nPos = self.__workSeqs[time].nPos
                stuff.workPos = nPos
                self.__workSeqs[time].nSeq[stuff.workPos] = stuff
                self.__workSeqs[time].nPos += 1
                stuff.sType = self.NOR
        else :
            msg = "员工工作: 类型错误. 当前类型为 {}.".format(wType)
            self.log(msg)
            raise errorclass.wrongType(msg)

        # 5.检查最大工作序号
        workPos = stuff.workPos
        if workPos > self.__maxWorkPos :
            self.__maxWorkPos = workPos

        # 6.清除等待位置
        stuff.waitPos = None

        # 7.添加工作位置
        self.__workSeqs[time].workPoses.append( (workPos, Id) )
        self.log("\n向第{}次时间队列 添加:员工工作位置:{}及工号:{}"\
                .format(time, workPos, Id))

        # 8.添加为改动员工
        self.__modStuffs.append(stuff)
        self.log(
            "\n{}员工工作操作完成!\t第{}次时间队列\t工作位置{}\t"\
            .format(Id, time, workPos))
