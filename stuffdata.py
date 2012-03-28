
#!/usr/bin/python3
# File Name : stuffData.py

from os import path
import pickle
import errorclass


__version__ = "0.3.1"


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
        self.wType = StuffContainer.IDLE
        self.sType = None


    def tell(self) :
        print("""我是{}号员工, 我叫{}, {}.处于第{}时间队列内.
我的工作类型是: {}, 队伍类型是: {}. 我的等待序号: {}, 工作序号: {}."""\
        .format(Id, name, gender, wTime,
            wType, sType, waitPos, workPos)

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
            print(msg)
            logfile = "./log.txt"
            try :
                log = open(logfile, "w")
                log.write(msg)
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

    #def getTimeSeq(self, time) ;
    #    return self.__workSeqs[time]

    #def getNSeq(self, time) :
    #    return self.__workSeqs[time].nSeq

    #def getSSeq(self, time) :
    #    return self.__workSeqs[time].sSeq

    #def getWSeq(self, time) :
    #    return self.__workSeqs[time].wSeq

    # 返回及设置位置 #

    #def getNPos(self, time) :
    #    return self.__workSeqs[time].nPos

    #def getSPos(self, time) :
    #    return self.__workSeqs[time].sPos

    #def getWPos(self, time) :
    #    return self.__workSeqs[time].wPos

    #def setNPos(self, time, nPos) :
    #    self.__workSeqs[time].nPos = nPos

    #def setSPos(self, time, sPos) :
    #    self.__workSeqs[time].sPos = sPos

    #def setWPos(self, time, wPos) :
    #    self.__workSeqs[time].wPos = wPos

    #def incNPos(self, time) :
    #    self.__workSeqs[time].nPos += 1

    #def incSPos(self, time) :
    #    self.__workSeqs[time].sPos += 1

    #def incWPos(self, time) :
    #    self.__workSeqs[time].wPos += 1

    # 基本操作 #
    def leaveWork(self, Id) :
        self.log("\n{}号员工脱离工作状态操作: ".format(Id))

        # 1.取得员工基本信息
        stuff = self.__stuffs[Id]
        time = stuff.wTime
        wType = stuff.wType
        sType = stuff.sType
        workPos = stuff.workPos
        self.log(
        "\n\n工作位置:{}, 工作次数:{}, 工作类型:{}, 队伍类型:{}"\
                     .format(workPos, time, wType, sType))

        # 2.脱离workPoses序列
        self.__workSeqs[time].workPoses.remove( (workPos, Id) )
        self.log("\n\n工号:{}, 脱离第{}次工作位置序列."\
                     .format(workPos, time))

        # 3.脱离workSeqs[time]
        if sType is self.NOR :
            self.__workSeqs[time].nSeq.pop(workPos)
            self.log("\n\n脱离NOR工作队伍.")
        elif sType is self.SEL :
            self.__workSeqs[time].sSeq.pop(workPos)
            self.log("\n\n脱离SEL工作队伍.")
        else :
            self.log("\n!!!---- 错误: 员工队伍类型有误----!!!")
            return

        # 4.操作完成.
        self.log("\n@@@---- 成功: 员工脱离工作状态! ----@@@")

    def leaveWait(self, Id) :
        self.log("\n{}号员工脱离等待状态操作: ".format(Id))

        # 1.取得员工基本信息
        stuff = self.__stuffs[Id]
        time = stuff.wTime
        wType = stuff.wType
        sType = stuff.sType
        waitPos = stuff.waitPos
        self.log(
        "\n\n工作位置:{}, 工作次数:{}, 工作类型:{}, 队伍类型:{}"\
                     .format(waitPos, time, wType, sType))

        # 2.脱离workSeq[time]
        if sType is not self.WAIT :
            self.log("\n!!!---- 错误: 员工队伍类型有误----!!!")
            raise errorclass.wrongType("员工队伍类型有误.")
        self.__workSeqs[time].wSeq.pop(waitPos)

        # 3.脱离waitPoses序列
        self.__workSeqs[time].waitPoses.remove( (waitPos, Id) )
        self.log("\n\n工号:{}, 脱离第{}次等待位置序列."\
                     .format(waitPos, time))

        # 4.操作完成
        self.log("\n@@@---- 成功: 员工脱离等待状态! ----@@@")

    def updateMax(self, Id, time) :
        self.log("\n{}号员工指定第{}次工作操作, 并自动更新: "\
        .format(Id, time))

        # 1.取得员工基本信息
        stuff = self.__stuffs[Id]
        self.log("\n员工工作次数:{}, 序列最大值: {}."\
         .format(stuff.wTime, self.__maxTime))

        # 2.设定员工工作序号为指定次数
        stuff.wTime = time

        # 3.判断是否超出当前最大值
        if time > self.__maxTime :
            self.__maxTime = time
            self.log("\n\n序列最大最大次数被更新: {}次"\
            .format(time))

            # 4.自动新增序列

            self.log("\n\n更新时间队列: 自动更新最大工作次数.")
            count = 0
            while len(self.__workSeqs) < ( time + 1 ) :
                self.__workSeqs.append(TimeSeq())
                count += 1
            self.log("\n@更新时间队列: 自动增加了{}列时间队列@"\
            .format(count))
        else :
            self.log("\n@@@----序列最大工作次数保持: {}次----@@@"\
            .format(time))

    def goWork(self, Id, wType) :
        self.log("\n\n{}号员工goWork操作.".format(Id))

        # 1.获得员工基本信息
        stuff = self.__stuffs[Id]

        # 2.设定员工工作类型
        stuff.wType = wType

        # 3.设定员工工作序号, 并更新序列中的序号
        # 4.加入对应工作队列
        # 5.设定员工队列类型

        if wType is self.NOR :
            # 3.设定员工工作序号, 并更新序列中的序号
            nPos = self.__workSeqs[time].nPos
            stuff.workPos = nPos 
            self.log("\n\n\n工作序号已设置为当前序列正常工作号: {}"\
                .format(nPos))
            self.__workSeqs[time].nPos += 1
            self.log("\n\n\n当前序列正常工作序号更新为 {}"\
                .format(self.__workSeqs[time].nPos))
            # 4.加入对应工作队列
            self.__workSeqs[time].nSeq[Id] = stuff
            # 5.设定员工队列类型
            stuff.sType = self.NOR
        elif wType is self.SEL :
            # 3.设定员工工作序号, 并更新序列中的序号
            waitPos = stuff.waitPos
            stuff.workPos = waitPos
            self.log("\n\n\n工作序号已设置为员工等待序号: {}"\
                .format(waitPos))
            self.__workSeqs[time].sPos = waitPos + 1
            self.log("\n\n\n当前序列选钟等待序号更新为 {}"\
                .format(self.__workSeqs[time].sPos))
            # 4.加入对应工作队列
            self.__workSeqs[time].sSeq[Id] = stuff
            # 5.设定员工队列类型
            stuff.sType = self.SEL
        elif wType is self.NAMED :
            if self.__workSeqs[time].sSeq :
                # 3.设定员工工作序号, 并更新序列中的序号
                sPos = self.__workSeqs[time].sPos
                stuff.workPos = sPos
                self.log("\n\n\n工作序号已设置为当前序列选钟序号: {}"\
                    .format(sPos))
                self.__workSeqs[time].sPos += 1
                self.log("\n\n\n当前序列选钟序号更新为 {}"\
                    .format(self.__workSeqs[time].sPos))
                # 4.加入对应工作队列
                self.__workSeqs[time].sSeq[Id] = stuff
                # 5.设定员工队列类型
                stuff.sType = self.SEL
            else :
                # 3.设定员工工作序号, 并更新序列中的序号
                nPos = self.__workSeqs[time].nPos
                stuff.workPos = nPos 
                self.log("\n\n\n工作序号已设置为当前序列正常工作号:{}"\
                    .format(nPos))
                self.__workSeqs[time].nPos += 1
                self.log("\n\n\n当前序列正常工作序号更新为 {}"\
                    .format(self.__workSeqs[time].nPos))
                # 4.加入对应工作队列
                self.__workSeqs[time].nSeq[Id] = stuff
                # 5.设定员工队列类型
                stuff.sType = self.NOR
        else :
            raise errorclass.wrongType("员工下一次工作类型有误.")

        # 6.清除等待序号
        stuff.waitPos = None
            
    # 复合操作 #
    def stuffWait(Id) :
        self.log("\n{}号员工进入等待状态操作: ".format(Id))

        # 1.获得员工基本信息
        stuff = self.__stuffs[Id]
        time = stuff.wTime
        wType = stuff.wType

        # 2.判断工作状态,确定是否需要脱离工作队伍
        if wType is self.NOR or self.SEL or self.NAMED :
            self.leaveWork(Id)
            # 3.脱离工作队伍, 将等待序号设置为当前工作序号(原位等待)
            stuff.waitPos = stuff.workPos
            # 4.将工作序号清除
            stuff.workPos = None
            self.log("\n\n等待序号已设置为当前工作序号: {}, 工作序号清零."\
            .format(stuff.waitPos))
        elif wType is self.IDLE :
            # 3.将等待序号设置为当前序列等待序号
            wPos = self.__workSeqs[time].wPos
            stuff.waitPos = wPos
            self.log("\n\n等待序号已设置为序列等待序号: {}."
            .format(wPos))
            # 4.更新当前序列等待序号
            self.__workSeqs[time].wPos += 1
            self.log("\n\n当前序列等待序号更新为: {}"\
            .format(self.__workSeqs[time].wPos))
        elif wType is self.WAIT :
            self.log("\n\n{}号员工已处于等待状态, 退出操作."format(Id))
            return

        # 5.更新 最大等待序号
        waitPos = stuff.waitPos
        if waitPos > self.__maxWaitPos :
            self.__maxWaitPos = waitPos
            self.log("\n\n员工等待序号为当前最大值.更新容器中最大值.")
        
        # 6.设置 工作状态为等待
        stuff.wType = self.WAIT
        self.log("\n\n员工工作状态改变: 等待.")

        # 7.加入 等待序列, 并更新等待序号序列
        self.__workSeqs[time].wSeq[Id] = stuff
        self.__workSeqs[time].waitPoses.append( (waitPos, Id) )
        self.log("\n\n员工被加入第{}此时间队列的等待序列, 并添加waitPoses"\
        .format(time))

        # 8.将员工序号加入 被更改员工队列
        self.__modStuffs.append(Id)
        self.log("\n\n员工进入等待状态操作已完成, 加入变动员工组")

        # 4.操作完成
        self.log("\n@@@---- 成功: 员工进入等待状态! ----@@@")

    def stuffJumpWork(Id, wType=NOR, time) :
        self.log("\n{}号员工进入工作状态操作: ".format(Id))

        # 1.获得员工基本信息
        stuff = self.__stuffs[Id]
        wTime = stuff.wTime
        #wType = stuff.wType

        # 2.员工脱离等待状态
        try :
            self.leaveWait(Id)
        except errorclass.wrongType :
            self.log("\n!!!---- 错误: 进入工作状态操作不成功----!!!")
            return
        self.updateMax(Id, time)

        # 3.设定员工工作类型, 加入工作队列, 设定队列类型
        #   并且 清除等待序号
        try :
            self.goWork(Id)
        except errorclass.wrongType :
            self.log("\n!!!---- 错误: 进入工作状态操作不成功----!!!")
            self.updateMax(Id, wTime)
            return

        # 4.更新最大工作序号
        workPos = stuff.workPos
        if workPos > self.__maxWorkPos :
            self.__maxWorkPos = workPos
            self.log("\n\n员工工作序号为当前最大值.更新容器中最大值.")

        # 5.更新工作序号序列
        self.workSeqs[time].workPoses.append( (workPos, Id) )
        self.log("\n\n员工被加入第{}此时间队列的工作序列, 并添加workPoses"\
        .format(time))

        # 6.将员工序号加入 变动员工组
        self.__modStuffs.append(Id)
        self.log("\n\n员工进入工作状态操作已完成, 加入变动员工组")

        # 7.操作完成
        self.log("\n@@@---- 成功: 员工进入工作状态! ----@@@")

    def stuffWork(Id, wType=NOR) :
        stuffJumpWork(Id, wType, self.__stuffs[Id].wTime + 1)

    # 批量操作 #
    def stuffsWait(self, *IDs)
        for Id in IDs :
            self.stuffWait(Id)

    def StuffsWork(self, wType=NOR, *IDs)
        for Id in IDs :
            self.stuffWork(Id, wType)


if __name__ == '__main__' :
    
    S = StuffContainer()


    startTime = time()
    S.addStuffs(S.MALE, 1,2,3,4,5,6,7,8,9)
    createTime = time()
    S.stuffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    S.reportStuffs()
    S.stuffsWork(S.NOR,1, 2, 3, 4, 5, 6, 7, 8, 9)
    stuffWorkTime = time()

    S.stuffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    S.stuffsWork(S.SEL, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    S.stuffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    stuffWork2Time = time()
    S.reportStuffs()
    endTime = time()
    print("""创建员工时间 {0} \n
员工第一次工作时间 {1}\n员工第二次工作时间 {2}
报告时间 {3}"""\
        .format((createTime - startTime),
            (stuffWorkTime - createTime),
            (stuffWork2Time - stuffWorkTime),
            (endTime - stuffWorkTime)))
    print("员工工号: {}".format(S.getIDs()))


    #S.save("/home/thedevil/test.qpc")
    #S.load("/home/thedevil/test.qpc")
