#!/usr/bin/python3
# File Name : staffData.py

from os import path
from time import time
import pickle
import errorclass


__version__ = "0.3.1"


DEBUG = True


class Staff :
    """包含员工的详细信息"""

    def __init__(self, Id, gender='男', name=None) :
        self.Id = Id
        self.gender = gender
        if name is not None :
            self.name = name
        else :
            self.name = ""
        self.waitPos = None
        self.workPos = None
        self.wTime = 0
        self.wType = StaffContainer.IDLE
        self.sType = None


    def tell(self) :
        print("""我是{}号员工, 我叫{}, {}.处于第{}时间队列内.
我的工作类型是: {}, 队伍类型是: {}. 我的等待序号: {}, 工作序号: {}."""\
        .format(self.Id, self.name, self.gender, self.wTime,
            self.wType, self.sType, self.waitPos, self.workPos))

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


class StaffContainer :
    """员工以及工作对列的容器"""

    MALE = '男'
    FEMALE = '女'

    NOR = '排钟'
    NAMED = '点钟'
    SEL = '选钟'
    WAIT = '等待'
    IDLE = '休息'

    workTypes = [NOR, SEL, NAMED]

    def __init__(self) :
        self.__IDs = []
        self.__staffs = {}
        self.__modStaffs = set()
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
        for staff in iter(self.__staffs.values()) :
            yield staff

    def __len__(self) :
        return len(self.__staffs)

    #------------------------#

    #---- 容器的简单函数 ----#

    #-- 返回及设置属性 --#

    def getIDs(self) :
        return self.__IDs

    def getStaff(self, Id) :
        return self.__staffs[Id]

    def getStaffs(self) :
        return self.__staffs

    def getModStaffs(self) :
        return self.__modStaffs

    def getWorkSeq(self) :
        return self.__workSeqs

    def getMaxTime(self) :
        return self.__maxTime

    def updateMaxTime(self, time) :
        self.log("\t更新最大工作次数:\t")
        if time > self.__maxTime :
            self.__maxTime = time
            self.log("更新为: {}!".format(time))
        else :
            self.log("保持不变: {}.".format(self.__maxTime))

    def getMaxId(self) :
        return self.__maxId

    def updateMaxId(self, Id) :
        self.log("\t更新最大工号:\t")
        if Id > self.__maxId :
            self.__maxId = Id
            self.log("更新为: {}!".format(Id))
        else :
            self.log("保持不变: {}.".format(self.__maxId))

    def getMaxWorkPos(self) :
        return self.__maxWorkPos

    def updateMaxWorkPos(self, workPos) :
        self.log("\t更新最大工作位置: \t")
        if workPos and workPos > self.__maxWorkPos :
            self.__maxWorkPos = workPos
            self.log("更新为: {}!".format(waitPos))
        else :
            self.log("保持不变: {}.".format(self.__maxWaitPos))

    def getMaxWaitPos(self) :
        return self.__maxWaitPos

    def updateMaxWaitPos(self, waitPos) :
        self.log("\t更新最大等待位置: \t")
        if waitPos and waitPos > self.__maxWaitPos :
            self.__maxWaitPos = waitPos
            self.log("更新为: {}!".format(waitPos))
        else :
            self.log("保持不变: {}.".format(self.__maxWaitPos))

    def getFilename(self) :
        return self.__fileName

    def setFilename(self, fileName) :
        self.__fileName = fileName

    def isDirty(self) :
        return self.__dirty

    def setDirty(self, dirty=True) :
        self.__dirty = dirty
        self.log("\t设置改动(__dirty): {}.".format(dirty))

    #--------------------#

    #---- 文件操作 ----#

    def log(self, msg) :
        if DEBUG :
            print(msg)
            logfile = "./log.txt"
            try :
                log = open(logfile, "a")
                log.write("\n"+msg)
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
            self.log("\t保存文件: 文件后缀正确!")
            return self.savePickle()
        msg = "\t保存文件: 文件后缀错误."
        self.log(msg)
        return False, msg 

    def savePickle(self) :
        error = None
        theFile = None
        try :
            theFile = open(self.__fileName, "wb")
            pickle.dump(self, fh)
        except EnvironmentError as e :
            error = "\t保存文件: 失败. 错误: {}".format(e)
            self.log(error)
        finally :
            if theFile is not None :
                theFile.close()
            if error is not None :
                return False, error
            msg = "\t保存文件: 成功!"
            self.log(msg)
            return True, msg

    def load(self, fileName="") :
        if fileName :
            self.__fileName = fileName
        if self.__fileName.endswith(".qpc") :
            self.log("\t读取文件: 文件后缀正确!")
            return self.loadPickle()
        msg = "\t读取文件: 文件后缀错误."
        self.log(msg)
        return False, msg

    def loadPickle(self) :
        error = None
        theFile = None
        staffs = None
        try :
            theFile = open(self.__fileName, "rb")
            self.clear(False)
            staffs = pickle.load(theFile)
        except EnvironmentError as e :
            error = "\t读取文件: 失败. 错误: {}".format(e)
            self.log(error)
        finally :
            if theFile is not None :
                theFile.close()
            if error is not None :
                return False, error
            self.dirty = False
            msg = "\t读取文件: 成功!"
            self.log(msg)
            return (True, msg, staffs)

    #------------------#

    #---- 时间队列 ----#

    #-- 操纵容器内时间队列 --#

    def addTimeSeq(self) :
        self.__workSeqs.append(TimeSeq())
        self.log("\t添加时间队列.")

    def updateMaxSeq(self, time) :
        if time > self.__maxTime :
            self.__maxTime = time
            self.log("\t更新时间队列: 自动更新最大工作次数.")
            count = 0
        while len(self.__workSeqs) < ( time + 1 ) :
            self.__workSeqs.append(TimeSeq())
            count += 1
        self.log("\t更新时间队列: 自动增加了{}列时间队列"\
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
        self.log("\t\t{}号员工脱离工作状态操作: ".format(Id))

        # 1.取得员工基本信息
        staff = self.__staffs[Id]
        time = staff.wTime
        wType = staff.wType
        sType = staff.sType
        workPos = staff.workPos
        self.log(
        "\t\t\t工作位置:{}, 工作次数:{}, 工作类型:{}, 队伍类型:{}"\
                     .format(workPos, time, wType, sType))

        # 2.脱离workPoses序列
        self.__workSeqs[time].workPoses.remove( (workPos, Id) )
        self.log("\t\t\t工号:{}, 脱离第{}次工作位置序列."\
                     .format(workPos, time))

        # 3.脱离workSeqs[time]
        if sType is self.NOR :
            # test only #
            for staff in self.__workSeqs[time].nSeq.values() :
                print(staff.Id, staff.workPos)
            self.__workSeqs[time].nSeq.pop(workPos)
            self.log("\t\t\t脱离NOR工作队伍.")
        elif sType is self.SEL :
            self.__workSeqs[time].sSeq.pop(workPos)
            self.log("\t\t\t脱离SEL工作队伍.")
        else :
            self.log("\t\t!!!---- 错误: 员工队伍类型有误----!!!")
            return

        # 4.操作完成.
        self.log("\t\t@@@---- 成功: 员工脱离工作状态! ----@@@")

    def leaveWait(self, Id) :
        self.log("\t\t{}号员工脱离等待状态操作: ".format(Id))

        # 1.取得员工基本信息
        staff = self.__staffs[Id]
        time = staff.wTime
        wType = staff.wType
        sType = staff.sType
        waitPos = staff.waitPos
        self.log(
        "\t\t\t工作位置:{}, 工作次数:{}, 工作类型:{}, 队伍类型:{}"\
                     .format(waitPos, time, wType, sType))

        # 2.脱离workSeq[time]
        if sType is not self.WAIT :
            self.log("\t\t!!!---- 错误: 员工队伍类型有误----!!!")
            raise errorclass.wrongType("员工队伍类型有误.")
        self.__workSeqs[time].wSeq.pop(waitPos)

        # 3.脱离waitPoses序列
        self.__workSeqs[time].waitPoses.remove( (waitPos, Id) )
        self.log("\t\t\t工号:{}, 脱离第{}次等待位置序列."\
                     .format(waitPos, time))

        # 4.操作完成
        self.log("\t\t@@@---- 成功: 员工脱离等待状态! ----@@@")

    def updateMax(self, Id, time) :
        self.log("\t\t{}号员工指定第{}次工作操作, 并自动更新: "\
        .format(Id, time))

        # 1.取得员工基本信息
        staff = self.__staffs[Id]
        self.log("\t\t员工工作次数:{}, 序列最大值: {}."\
         .format(staff.wTime, self.__maxTime))

        # 2.设定员工工作序号为指定次数
        staff.wTime = time

        # 3.判断是否超出当前最大值
        if time > self.__maxTime :
            self.__maxTime = time
            self.log("\t\t\t序列最大最大次数被更新: {}次"\
            .format(time))

            # 4.自动新增序列

            self.log("\t\t\t更新时间队列: 自动更新最大工作次数.")
            count = 0
            while len(self.__workSeqs) < ( time + 1 ) :
                self.__workSeqs.append(TimeSeq())
                count += 1
            self.log("\t\t@更新时间队列: 自动增加了{}列时间队列@"\
            .format(count))
        else :
            self.log("\t\t@@@----序列最大工作次数保持: {}次----@@@"\
            .format(time))

    def goWork(self, Id, wType) :
        self.log("\t\t{}号员工goWork操作.".format(Id))

        # 1.获得员工基本信息
        staff = self.__staffs[Id]
        time = staff.wTime

        # 2.设定员工工作类型
        staff.wType = wType

        # 3.设定员工工作序号, 并更新序列中的序号
        # 4.加入对应工作队列
        # 5.设定员工队列类型

        if wType is self.NOR :
            # 3.设定员工工作序号, 并更新序列中的序号
            nPos = self.__workSeqs[time].nPos
            staff.workPos = nPos 
            self.log("\t\t\t工作序号已设置为当前序列正常工作号: {}"\
                .format(nPos))
            self.__workSeqs[time].nPos += 1
            self.log("\t\t\t当前序列正常工作序号更新为 {}"\
                .format(self.__workSeqs[time].nPos))
            # 4.加入对应工作队列
            self.__workSeqs[time].nSeq[nPos] = staff
            # 5.设定员工队列类型
            staff.sType = self.NOR
        elif wType is self.SEL :
            # 3.设定员工工作序号, 并更新序列中的序号
            waitPos = staff.waitPos
            staff.workPos = waitPos
            self.log("\t\t\t工作序号已设置为员工等待序号: {}"\
                .format(waitPos))
            self.__workSeqs[time].sPos = waitPos + 1
            self.log("\t\t\t当前序列选钟等待序号更新为 {}"\
                .format(self.__workSeqs[time].sPos))
            # 4.加入对应工作队列
            self.__workSeqs[time].sSeq[waitPos] = staff
            # 5.设定员工队列类型
            staff.sType = self.SEL
        elif wType is self.NAMED :
            if self.__workSeqs[time].sSeq :
                # 3.设定员工工作序号, 并更新序列中的序号
                sPos = self.__workSeqs[time].sPos
                staff.workPos = sPos
                self.log("\t\t\t工作序号已设置为当前序列选钟序号: {}"\
                    .format(sPos))
                self.__workSeqs[time].sPos += 1
                self.log("\t\t\t当前序列选钟序号更新为 {}"\
                    .format(self.__workSeqs[time].sPos))
                # 4.加入对应工作队列
                self.__workSeqs[time].sSeq[sPos] = staff
                # 5.设定员工队列类型
                staff.sType = self.SEL
            else :
                # 3.设定员工工作序号, 并更新序列中的序号
                nPos = self.__workSeqs[time].nPos
                staff.workPos = nPos 
                self.log("\t\t\t工作序号已设置为当前序列正常工作号:{}"\
                    .format(nPos))
                self.__workSeqs[time].nPos += 1
                self.log("\t\t\t当前序列正常工作序号更新为 {}"\
                    .format(self.__workSeqs[time].nPos))
                # 4.加入对应工作队列
                self.__workSeqs[time].nSeq[nPos] = staff
                # 5.设定员工队列类型
                staff.sType = self.NOR
        else :
            raise errorclass.wrongType("员工下一次工作类型有误.")

        # 6.清除等待序号
        staff.waitPos = None
            
    # 复合操作 #
    def updateStaff(self, Id, 
            gender=None, name=None) :
        self.log("\t更新员工操作: ")

        # 1.判断员工工号是否存在
        if Id not in self.__staffs :
            self.log("\t\t没有工号为: {}号的员工, 添加员工.")
            self.__staffs[Id] = Staff(Id)
            self.__IDs.append(Id)
            self.__IDs.sort()
            # 2.判断员工工号是否为最大值
            if Id > self.__maxId :
                self.__maxId = Id
            # 3.设置员工工作类型为空闲
            self.__staffs[Id].wType = self.IDLE

        # 4.获得员工
        staff = self.__staffs[Id]

        # 5.更新员工信息
        if gender is not None :
            staff.gender = gender
        if name is not None :
            staff.name = name
        self.log("\t\t工号为: {}的员工, 姓名:{}, 性别: {}."\
            .format(Id, name, gender))

        # 6.将员工添加至 变动员工组
        self.__modStaffs.add(staff)

        # 7.设置容器状态为已改变
        self.__dirty = True

        self.log("\t@@@---- 成功: 更新员工信息 ----@@@")

    def deleteStaff(self, Id) :
        self.log("\t删除员工操作: ")

        # 1.判断员工是否存在
        if Id not in self.__staffs :
            return
        
        # 2.获得员工信息
        staff = self.__staffs[Id]
        time = staff.wTime
        wType = staff.wType
        self.log("\t\t员工工号为: {}, 工作类型为: {}, 队伍类型为: {}"\
            .format(Id, wType, sType))

        # 3.判断员工工作状态, 利用相应基本操作退出状态
        if wType in self.workTypes :
            self.leaveWork(Id)
        elif wType is self.WAIT :
            self.leaveWait(Id)
        else :      # 员工处于休息状态, 可以直接移除
            pass
        
        # 4.从 员工队列 中移除员工
        del self.__staffs[Id]
        self.log("\t\t从员工队列中移除工号为: {}的员工."\
            .format(Id))

        # 5.从 工号队列 中移除员工工号
        self.__IDs.remove(Id)
        self.log("\t\t从工号队列中移除工号为: {}的员工."\
            .format(Id))

        # 6.将员工加入 变动员工组
        self.__modStaffs.add(Id)

        # 7.操作完成, 设置 dirty
        self.log("\t@@@---- 成功: 移除员工 ----@@@")
        self.__dirty = True
            

    def staffWait(self, Id) :
        self.log("\t{}号员工进入等待状态操作: ".format(Id))

        # 1.获得员工基本信息
        staff = self.__staffs[Id]
        time = staff.wTime
        wType = staff.wType

        # 2.判断工作状态,确定是否需要脱离工作队伍
        #if (wType is self.NOR or wType is self.SEL or
        #    wType is self.NAMED ) :
        if wType in self.workTypes :
            self.leaveWork(Id)
            # 3.脱离工作队伍, 将等待序号设置为当前工作序号(原位等待)
            staff.waitPos = staff.workPos
            # 4.将工作序号清除
            staff.workPos = None
            self.log("\t\t等待序号已设置为当前工作序号: {}, 工作序号清零."\
            .format(staff.waitPos))
        elif wType is self.IDLE :
            # 3.将等待序号设置为当前序列等待序号
            wPos = self.__workSeqs[time].wPos
            staff.waitPos = wPos
            self.log("\t\t等待序号已设置为序列等待序号: {}."
            .format(wPos))
            # 4.更新当前序列等待序号
            self.__workSeqs[time].wPos += 1
            self.log("\t\t当前序列等待序号更新为: {}"\
            .format(self.__workSeqs[time].wPos))
        elif wType is self.WAIT :
            self.log("\t\t{}号员工已处于等待状态, 退出操作."\
                .format(Id))
            return
        else :
            raise errorclass.wrongType("员工工作类型有误. {}"\
                .format(wType))

        # 5.更新 最大等待序号
        waitPos = staff.waitPos
        #if waitPos and waitPos > self.__maxWaitPos :
        if waitPos > self.__maxWaitPos :
            self.__maxWaitPos = waitPos
            self.log("\t\t员工等待序号为当前最大值.更新容器中最大值.")
        
        # 6.设置 工作状态为等待, 队列类型为等待
        staff.wType = self.WAIT
        staff.sType = self.WAIT
        self.log("\t\t员工工作状态改变: 等待.")

        # 7.加入 等待序列, 并更新等待序号序列
        self.__workSeqs[time].wSeq[Id] = staff
        self.__workSeqs[time].waitPoses.append( (waitPos, Id) )
        self.log("\t\t员工被加入第{}此时间队列的等待序列, 并添加waitPoses"\
        .format(time))

        # 8.将员工序号加入 被更改员工队列
        self.__modStaffs.add(staff)
        self.log("\t\t员工进入等待状态操作已完成, 加入变动员工组")

        # 9.操作完成
        self.log("\t@@@---- 成功: 员工进入等待状态! ----@@@")

        # 10. dirty
        self.__dirty = True

    def staffJumpWork(self, Id, time, wType=NOR) :
        self.log("\t{}号员工进入工作状态操作: ".format(Id))

        # 1.获得员工基本信息
        staff = self.__staffs[Id]
        wTime = staff.wTime
        #wType = staff.wType

        # 2.员工脱离等待状态
        try :
            self.leaveWait(Id)
        except errorclass.wrongType :
            self.log("\t!!!---- 错误: 进入工作状态操作不成功----!!!")
            return
        self.updateMax(Id, time)

        # 3.设定员工工作类型, 加入工作队列, 设定队列类型
        #   并且 清除等待序号
        try :
            self.goWork(Id, wType)
        except errorclass.wrongType :
            self.log("\t!!!---- 错误: 进入工作状态操作不成功----!!!")
            self.updateMax(Id, wTime)
            return

        # 4.更新最大工作序号
        workPos = staff.workPos
        if workPos and workPos > self.__maxWorkPos :
            self.__maxWorkPos = workPos
            self.log("\t\t员工工作序号为当前最大值.更新容器中最大值.")

        # 5.更新工作序号序列
        self.__workSeqs[time].workPoses.append( (workPos, Id) )
        self.log("\t\t员工被加入第{}此时间队列的工作序列, 并添加workPoses"\
        .format(time))

        # 6.将员工序号加入 变动员工组
        self.__modStaffs.add(staff)
        self.log("\t\t员工进入工作状态操作已完成, 加入变动员工组")

        # 7.操作完成
        self.log("\t@@@---- 成功: 员工进入工作状态! ----@@@")
        self.__dirty = True

    def staffWork(self, Id, wType=NOR) :
        self.staffJumpWork(Id,
            self.__staffs[Id].wTime + 1, wType)

    # 批量操作 #
    def addStaffs(self, gender, *IDs) :
        for Id in IDs :
            self.updateStaff(Id,gender)

    def staffsWait(self, *IDs) :
        for Id in IDs :
            self.staffWait(Id)

    def staffsWork(self, wType=NOR, *IDs) :
        for Id in IDs :
            self.staffWork(Id, wType)

    # 调试 #
    def reportStaffs(self) :
        """汇报当前正在工作的员工情况."""
        print("含有{0}名员工.".format(len(S)))
        for workSeq in self.__workSeqs :
            if 1 :
                print("第{0}次工作队列 \t"\
                    .format(self.__workSeqs.index(workSeq)))
                print()
                print("正常上班序列")
                print("当前上班班号: {0}"\
                    .format(workSeq.nPos))
                for staff in workSeq.nSeq.values() :
                    print(
                    "员工工号: {0} 上班号码: {1} 上班次数:{2}"\
                    .format(staff.Id,
                    staff.workPos, staff.wTime))
                print()
                print("选钟后上班序列")
                print("当前上班班号: {0}"\
                    .format(workSeq.sPos))
                for staff in workSeq.sSeq.values() :
                    print(
                    "员工工号: {0} 上班号码: {1} 上班次数:{2}"\
                    .format(staff.Id,
                    staff.workPos, staff.wTime))
                print()
                print("等待员工")
                print("当前等待班号: {0}"\
                    .format(workSeq.wPos))
                for staff in workSeq.wSeq.values() :
                    print(
                    "员工工号: {0} 等待号码: {1} 上班次数:{2}"\
                    .format(staff.Id,
                    staff.waitPos, staff.wTime))
        print("\n END ")
        print("最大工作次数: {0}".format(S.getMaxTime()))

if __name__ == '__main__' :
    
    S = StaffContainer()
    S.log("\nAGAIN")


    startTime = time()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9)
    createTime = time()
    S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    S.reportStaffs()
    S.staffsWork(S.NOR,1, 2, 3, 4, 5, 6, 7, 8, 9)
    staffWorkTime = time()

    S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    S.staffsWork(S.SEL, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    staffWork2Time = time()
    S.reportStaffs()
    endTime = time()
    print("""创建员工时间 {0} \n
员工第一次工作时间 {1}\n员工第二次工作时间 {2}
报告时间 {3}"""\
        .format((createTime - startTime),
            (staffWorkTime - createTime),
            (staffWork2Time - staffWorkTime),
            (endTime - staffWorkTime)))
    print("员工工号: {}".format(S.getIDs()))


    S.staffsWork(S.NOR, 4, 5, 6)
    S.staffsWork(S.NAMED, 7, 8)
    S.getStaffs()[1].tell()
    S.staffsWork(S.SEL, 1, 2, 3)
    S.staffsWork(S.NAMED, 5, 6)
    S.staffsWork(S.SEL, 9)
    S.reportStaffs()
    S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    S.reportStaffs()

    S.save("/home/thedevil/test.qpc")
    S.load("/home/thedevil/test.qpc")
