#!/usr/bin/python3
# File Name : staffData.py

# 文件 #
import pickle

from os import path

# 时间 #
from time import time

# 错误 #
from errorclass import *


__version__ = "0.3.1"


DEBUG = True
PRINT = True


class Staff :
    """包含员工的详细信息"""

    def __init__(self, Id, gender='男', name="") :
        self.Id = Id
        self.gender = gender
        self.name = name
        self.wTime = 0
        self.wType = StaffContainer.IDLE
        self.sType = StaffContainer.IDLE


    def tell(self) :
        print("""我是{}号员工, 我叫{}, {}.处于第{}时间队列内.
我的工作类型是: {}."""\
        .format(self.Id, self.name, self.gender, self.wTime,
            self.wType))

class TimeSeq :
    """包含不同工作次数的员工"""

    def __init__(self) :
        self.nPos = [0]
        self.sPos = [0]
        self.selected = False
        self.nSeq = [None]


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
        self.__unGrpIDs = []
        self.__groups = [ [] ] * 3
        self.__workGroup = None
        self.__staffs = {}
        self.__modStaffs = set()
        self.__workSeqs = []
        self.__maxTime = 0
        self.__maxId = 0
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

    def clear(self, clearFilename=True) :
        self.log("\t清除容器操作: ")
        self.__IDs = []
        self.__staffs = {}
        self.__modStaffs = set()
        self.__workSeqs = []
        self.__maxTime = 0
        self.__maxId = 0
        if clearFilename :
            self.__fileName = ""
            self.log("\t\t清除文件名.")
        self.addTimeSeq()

        self.__dirty = True
        self.log("\t@@@---成功: 清除容器---@@@\n\n")

    #-- 返回及设置属性 --#

    def getIDs(self) :
        return self.__IDs

    def getUngrpStaff(self) :
        return self.__unGrpIDs

    def getGroups(self) :
        return self.__groups

    def getWorkGroup(self) :
        return self.__workGroup

    def setWorkGroup(self, workGroup) :
        self.__workGroup = workGroup

    def getStaff(self, Id) :
        if Id in self.__staffs :
            return self.__staffs[Id]
        else :
            return False

    def getStaffs(self) :
        return self.__staffs

    def getModStaffs(self) :
        return self.__modStaffs

    def getWorkSeq(self) :
        return self.__workSeqs

    def getMaxTime(self) :
        return self.__maxTime

    def getMaxId(self) :
        return self.__maxId

    def getMaxWorkPos(self) :
        maxWorkPos = 0
        for workSeq in self.__workSeqs :
            maxNPos = max(nPos)
            if  maxNPos > maxWorkPos :
                maxWorkPos = maxNPos
        return maxNPos

    def updateMaxId(self, Id) :
        self.log("\t更新最大工号:\t")
        if Id > self.__maxId :
            self.__maxId = Id
            self.log("更新为: {}!".format(Id))
        else :
            self.log("保持不变: {}.".format(self.__maxId))

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
            if PRINT :
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
        fh = None
        try :
            fh = open(self.__fileName, "wb")
            pickle.dump(self, fh)
        except EnvironmentError as e :
            error = "\t保存文件: 失败. 错误: {}".format(e)
            self.log(error)
        finally :
            if fh is not None :
                fh.close()
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
        fh = None
        staffs = None
        try :
            fh = open(self.__fileName, "rb")
            self.clear(False)
            staffs = pickle.load(fh)
            print("{}".format("no" if staffs is None else "YES"))
        except Exception as e :
            error = "\t读取文件: 失败. 错误: {}".format(e)
            self.log(error)
        finally :
            if fh is not None :
                fh.close()
            if error is not None :
                return False, error, StaffContainer()
            self.__dirty = False
            msg = "\t读取文件: 成功!\n staffs: {}".format(staffs)
            self.log(msg)
            return True, msg, staffs

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

    # 基本操作 #

    def groupStaff(self, Id, grpNum) :
        self.log("\t\t{}号员工分组(第{}组)操作:"\
            .format(Id, grpNum))
        # 1. 初始化局部变量
        unGrpIDs = self.__unGrpIDs
        groups = self.__groups
        staff = self.getStaff(Id)

        # 2. 检查员工是否处于 IDLE 状态
        if staff.wType == self.IDLE :
            msg = "员工状态错误.\n需要在空闲态才能分组."
            self.log(msg)
            raise wrongType(msg)

        # 3. 将员工序号从 未分组员工中弹出
        if Id in unGrpIDs :
            unGrpIDs.remove(Id)
        else :
            msg = "!!!----分组失败: 员工不在未分组员工中."
            self.log(msg)
            raise notFoundInGroup(msg)

        # 4. 将员工序号插入分组
        # 4.1 检测分组是否存在 并且 更新分组
        while len(groups) < (grpNum + 1) :
            groups.append([])
        # 4.2 将员工放入分组, 并且使员工处于等待状态.
        groups[grpNum].append(Id)
        self.staffWait(Id)
        self.log("\t\t员工进入第{}组分组.".format(grpNum))
        
        # 5. 操作完成
        self.log("\t\t@@@----成功: 员工进入分组.----@@@")

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

    def norWork(self, Id) :
        self.log("\t\t{}员工正常上班操作:".format(Id))

        # 1. 初始化局部变量
        staff = self.__staffs[Id]
        wTime = staff.wTime
        wType = staff.wType
        workSeqs = self.__workSeqs
        workSeq = workSeqs[wTime]
        nSeq = workSeq.nSeq

        # 2. 判断员工当前状态是否为等待状态
        if wType is not self.WAIT :
            self.log("\t\t!!!----失败: 员工当前状态错误----!!!")
            raise notWaiting("!!!----失败: 员工当前状态错误----!!!")

        # 3. 使员工脱离工作队列
        pos = nSeq.index(staff)
        nSeq.remove(staff)
        nSeq.insert(pos, None)
        self.log("\t\t员工脱离第{}次工作队列.".format(wTime))

        # 4. 更新工作次数
        staff.wTime += 1
        wTime = staff.wTime
        self.updateMaxSeq(wTime)
        workSeq = workSeqs[wTime]
        nSeq = workSeq.nSeq

        # 5. 更新状态
        staff.wType = self.NOR
        staff.sType = self.NOR
        self.log("\t\t员工当前工作次数: {}, 工作状态: {}"\
            .format(staff.wTime, staff.wType))

        # 6. 员工按照序列正常工作序号, 进入序列
        # 6.1 取得当前序列正常工作序号
        nPos = ( max(workSeq.nPos) + 1 )
        # 6.2 检查当前序列长度
        checked = False
        while len(nSeq) <= nPos :
            self.__workSeqs[wTime].nSeq.append(None)
            if not checked :
                self.log("\t\t当前工作序列长度小于工作序号, 自动增加中.")
                checked = True
        # 6.3 判断工作位置状态
        inPos = nSeq[nPos]
        if inPos is None :
            nSeq[nPos] = staff
            self.log("\t\t员工工作位置为空, 正常上班.")
        elif isinstance(inPos, Staff) and inPos.wType is self.SEL :
            nSeq.insert(nPos, staff)
            self.log("\t\t员工工作位置非空为选钟员工, 插队上班.")
        else :
            self.log("\t\t!!!----错误: 插入员工时出现未知错误.----!!!")
            raise norWork("!!!----错误: 插入员工时出现未知错误.----!!!")

        # 7. 更新队列工作序号
        if nPos not in workSeq.nPos :
            workSeq.nPos.append( nPos )
        self.log("\t\t向第{}次时间队列添加 nPos :　{}."\
            .format(wTime, nPos))

        # 8. 判断是否需要更新 sPos
        sPos = self.__workSeqs[wTime].sPos
        if nPos <= max(sPos) :
            self.log("\t\t更新 sPos.未更新的 sPos: {}"\
                .format(sPos))
            self.__workSeqs[wTime].sPos = \
                [i for i in sPos if i<nPos] + [i+1 for i in sPos if i>= nPos]
            sPos = self.__workSeqs[wTime].sPos
            self.log("\t\t更新 sPos.更新后的 sPos: {}"\
                .format(sPos))
        
        # 8. 加入变动员工组
        self.__modStaffs.add(staff)

        # 9. 操作完成, 设置文件改动
        self.log("\t\t@@@---- 成功: 员工正常上班操作 ----@@@")
        self.__dirty = True

    def selWork(self, Id) :
        self.log("\t\t{}号员工选钟上班工作:".format(Id))

        # 1. 初始化局部变量
        staff = self.__staffs[Id]
        wTime = staff.wTime
        wType = staff.wType
        workSeqs = self.__workSeqs
        workSeq = workSeqs[wTime]
        nSeq = workSeq.nSeq

        # 2. 判断员工当前状态是否为等待状态
        if wType is not self.WAIT :
            self.log("\t\t!!!----失败: 员工当前状态错误----!!!")
            raise notWaiting("!!!----失败: 员工当前状态错误----!!!")

        # 3. 提取当前工作序号, 使员工脱离工作队列
        # 3.1 判断员工工作状态
        pos = nSeq.index(staff)
        nSeq.remove(staff)
        nSeq.insert(pos, None)
        self.log("\t\t员工脱离第{}次工作队列, 工作序号: {}."\
            .format(wTime, pos))

        # 4. 更新工作次数
        staff.wTime += 1
        wTime = staff.wTime
        self.updateMaxSeq(wTime)
        workSeq = workSeqs[wTime]
        nSeq = workSeq.nSeq

        # 5. 更新状态
        staff.wType = self.SEL
        staff.sType = self.SEL
        self.log("\t\t员工当前工作次数: {}, 工作状态: {}"\
            .format(staff.wTime, staff.wType))

        # 6. 员工按照上次序列工作序号, 进入序列
        # 6.1 已取得当前工作序号
        # 6.2 检查当前序列长度
        checked = False
        while len(nSeq) <= pos :
            nSeq.append(None)
            if not checked :
                self.log("\t\t当前工作序列长度小于工作序号, 自动增加中.")
                checked = True
        # 6.3 判断工作位置状态, 插入队伍
        inPos = nSeq[pos]
        if inPos is None :
            nSeq[pos] = staff
        else :
            nSeq.insert(pos, staff)

        # 7. 更新 selected 状态, 更新 sPos
        sPos = workSeq.sPos
        if pos <= max(sPos) :
            self.log("\t\t更新 sPos.未更新的 sPos: {}"\
                .format(sPos))
            self.__workSeqs[wTime].sPos = \
                [i for i in sPos if i < pos] \
                    + [i+1 for i in sPos if i>= pos]
            sPos = self.__workSeqs[wTime].sPos
            self.log("\t\t更新 sPos.未更新的 sPos: {}"\
                .format(sPos))
        if pos not in sPos :
            workSeq.sPos.append( pos )
        self.log("\t\t向第{}次时间队列添加 sPos :　{}."\
            .format(wTime, pos))

        # 8. 判断是否需要更新 nPos
        nPos = self.__workSeqs[wTime].nPos
        if pos < max(nPos) :
            workSeq.nPos = [i for i in nPos if i < pos] \
                + [i+1 for i in nPos if i >= pos]
        else :
            if not workSeq.selected :
                workSeq.selected = True


        # 9. 加入变动员工组
        self.__modStaffs.add(staff)
        
        # 10. 操作完成, 设置文件改动
        self.log("\t\t@@@---- 成功: 员工选钟上班操作 ----@@@")
        self.__dirty = True

    def namedWork(self, Id) :
        self.log("\t\t{}号员工点钟上班工作:".format(Id))

        # 1. 初始化局部变量
        staff = self.__staffs[Id]
        wTime = staff.wTime
        wType = staff.wType
        workSeqs = self.__workSeqs
        workSeq = workSeqs[wTime]
        nSeq = workSeq.nSeq

        # 2. 判断员工当前状态是否为等待状态
        if wType is not self.WAIT :
            self.log("\t\t!!!----失败: 员工当前状态错误----!!!")
            raise notWaiting("!!!----失败: 员工当前状态错误----!!!")

        # 3. 使员工脱离工作队列
        pos = self.__workSeqs[wTime].nSeq.index(staff)
        nSeq.remove(staff)
        nSeq.insert(pos, None)
        self.log("\t\t员工脱离第{}次工作队列.".format(wTime))

        # 4. 更新工作次数
        staff.wTime += 1
        wTime = staff.wTime
        self.updateMaxSeq(wTime)
        workSeq = workSeqs[wTime]
        nSeq = workSeq.nSeq

        # 5. 更新状态
        staff.wType = self.NAMED
        self.log("\t\t员工当前工作次数: {}, 工作状态: {}"\
            .format(staff.wTime, staff.wType))

        # 6. 员工按照序列正常工作序号进入序列
        # 6.1 取得当前序列正常工作序号
        nPos = ( max(workSeq.nPos) + 1 )
        sPos = ( max(workSeq.sPos) + 1 )
        #nPos = ( max(self.__workSeqs[wTime].nPos) )
        #sPos = ( max(self.__workSeqs[wTime].sPos) )
        # 6.2 判断 checked 状态
        if workSeq.selected : # 有选钟, 放在队列末尾
            self.log("\t\t有员工被选钟.且并非为插入正常工作序列中.")
            self.log("\t\t员工工作位置 sPos: {}."\
                .format(sPos))
            # 6.3 检查序列长度
            checked = False
            while len(nSeq) <= sPos :
                nSeq.append(None)
                if not checked :
                    self.log("\t\t当前工作序列长度小于工作序号, 自动增加中.")
                    checked = True
            if isinstance(nSeq[sPos-1], Staff)\
                    and nSeq[sPos-1].wType == self.SEL :
                inPos = nSeq[sPos]
                if inPos is None :
                    self.log("\t\t员工正常上点钟!")
                    self.__workSeqs[wTime].\
                    nSeq[sPos] = staff
                    self.__workSeqs[wTime].\
                    sPos.append(sPos)
                    staff.sType = self.SEL
                else :
                    self.log("\t\t员工工作位置非空.退出.")
                    raise namedWrong("员工工作位置非空.退出.")
            else :
                self.log("\t\t员工上一个位置并非SEL.退出.")
                raise namedWrong("员工上一个位置并非SEL.退出.")

        else :  # 无选钟插在中间
            self.log("\t\t无员工被选钟.")
            self.log("\t\t员工工作位置 nPos: {}."\
                .format(nPos))
            # 6.3 检查序列长度
            checked = False
            while len(nSeq) <= nPos :
                nSeq.append(None)
                if not checked :
                    self.log("\t\t当前工作序列长度小于工作序号, 自动增加中.")
                    checked = True
            inPos = nSeq[nPos-1]
            if inPos is None or (isinstance(inPos, Staff) and inPos.wType == self.NOR) :
                inPos = nSeq[nPos]
                if inPos is None :
                    self.log("\t\t员工正常上点钟!")
                    nSeq[nPos] = staff
                    workSeq.nPos.append(nPos)
                    staff.sType = self.NOR
                else :
                    self.log("员工工作位置异常.退出.")
                    raise namedWrong("员工工作位置异常.退出.")

            else :
                self.log("员工上一个位置非空或者不是NOR.退出.")
                raise namedWrong("员工上一个位置非空或者不是NOR.退出.")

        # 7. 加入变动员工组
        self.__modStaffs.add(staff)

        # 8. 操作完成, 设置文件改动
        self.log("\t\t@@@---- 成功: 员工点钟上班操作 ----@@@")
        self.__dirty = True

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
            self.__unGrpIDs.append(Id)
            self.__unGrpIDs.sort()
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
        sType = staff.sType
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

        # 6.从 工号队列 中移除员工工号
        if Id in self.__unGrpIDs :
            self.__unGrpIDs.remove(Id)
            found = True
        else :
            found = False
            for group in self.__groups :
                if Id in group :
                    found = True
                    group.remove(Id)
        if not found :
            msg = "!!!----员工组内未找到员工.----!!!"
            self.log(msg)
            raise notFoundInGroup(msg)
        self.log("\t\t从员工组中移除工号为: {}的员工."\
            .format(Id))

        # 7.将员工加入 变动员工组
        self.__modStaffs.add(Id)

        # 8.操作完成, 设置 dirty
        self.log("\t@@@---- 成功: 移除员工 ----@@@")
        self.__dirty = True
            
    def staffWait(self, Id) :
        self.log("\t{}号员工等待操作:".format(Id))

        # 1. 获得员工信息
        staff = self.__staffs[Id]
        wTime = staff.wTime
        wType = staff.wType
        sType = staff.sType

        # 2. 判断员工当前状态
        if wType is self.WAIT :
            self.log("\t@@@--员工已经处于等待状态, 无任何操作退出--@@@")
            return
        elif wType in self.workTypes :
            staff.wType = self.WAIT
            pos = self.__workSeqs[wTime].nSeq.index(staff)
            self.log("\t\t员工当前位置: {}.".format(pos))
        elif wType is self.IDLE :
            staff.wType = self.WAIT
            self.__workSeqs[0].nSeq.append(staff)

            
        # 3. 加入变动员工组
        self.__modStaffs.add(staff)

        # 4. 操作成功
        self.log("\t@@@----成功: 员工等待操作----@@@")
        self.__dirty = True

    def staffWork(self, Id, wType=NOR) :
        self.log("\t{}员工{}工作操作:".format(Id, wType))

        # 1. 获得员工信息
        staff = self.__staffs[Id]
        wTime = staff.wTime
        t_wType = staff.wType
        sType = staff.sType

        # 2. 检查员工当前状态是否为等待状态
        if t_wType != self.WAIT :
            self.log("\t员工不在等待状态, 结束操作.")
            return

        # 3. 更新 nPos, sPos
        pos = self.__workSeqs[wTime].nSeq.index(staff)
        if sType is self.NOR :
            self.__workSeqs[wTime].nPos.remove( pos )
            self.log("\t移除员工 nPos : {}.".format( pos ))
        elif sType is self.SEL :
            self.__workSeqs[wTime].sPos.remove( pos )
            self.log("\t移除员工 sPos : {}.".format( pos ))
        else :
            self.log("\t@@@--员工处于空闲态({}), 无 pos, 无操作."\
            .format(sType))

        if wType is self.NOR :
            self.norWork(Id)
        elif wType is self.SEL :
            self.selWork(Id)
        elif wType is self.NAMED :
            self.namedWork(Id)
        else :
            raise workWrong("需要工作的工作类型错误.")

        self.log("\t@@@----成功: 员工上班操作----@@@")
        self.__dirty = True

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
        print()
        for workSeq in self.__workSeqs :
            nSeq = workSeq.nSeq
            #nPos = max(workSeq.nPos)
            #sPos = max(workSeq.sPos)
            nPos = (workSeq.nPos)
            sPos = (workSeq.sPos)
            selected = workSeq.selected
            wTime = self.__workSeqs.index(workSeq)
            print("第{}次时间序列, nPos = {}, sPos = {}, {}选钟工作员工(非插入工作队列).".format(wTime, nPos, sPos, "有" if selected else "没有"))
            staffs = []
            for staff in nSeq :
                if staff is None :
                    staffs.append("空  ")
                else :
                    staffs.append("{}  ".format(staff.Id))
            msg = "".join(["员工序号: {}".format(Id) for Id in staffs])
            print(msg)
            print()

if __name__ == '__main__' :

    # 容器初始化
    S = StaffContainer()
    # 清除容器
    S.clear()
    # 添加员工
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9,)
    # 全部等待
    S.staffsWait(1,2,3,4,5,6,7,8,9)
    # 汇报情况
    S.reportStaffs()
    
    # 测试 全部正常工作
    S.staffsWork(S.NOR, 1,2,3,4,5,6,7,8,9)
    S.reportStaffs()

    # 重建测试环境
    S.clear()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9,)
    S.staffsWait(1,2,3,4,5,6,7,8,9)
    # 测试 全部选钟工作
    S.staffsWork(S.SEL, 1,2,3,4,5,6,7,8,9)
    S.reportStaffs()

    # 重建测试环境
    S.clear()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9,)
    S.reportStaffs()
    S.staffsWait(1,2,3,4,5,6,7,8,9)
    # 测试 1N, 3N, 4N, 2S(应在 1,3 之间)
    S.staffsWork(S.NOR, 1,3,4,5,6,7,9)
    S.reportStaffs()
    S.staffsWork(S.SEL, 2)
    S.reportStaffs()
    S.staffsWork(S.NAMED, 8)
    S.reportStaffs()

    # 重建测试环境
    S.clear()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9,)
    S.reportStaffs()
    S.staffsWait(1,2,3,4,5,6,7,8,9)
    # 测试 1N, 2S, 3S, 4N, 5N
    S.staffsWork(S.NOR, 1,4,5,6,7,8,9)
    S.reportStaffs()
    S.staffsWork(S.SEL, 2,3)
    S.reportStaffs()

    # 重建测试环境
    print()
    print()
    print()
    S.clear()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9,)
    S.reportStaffs()
    S.staffsWait(1,2,3,4,5,6,7,8,9)
    # 测试 多个员工同一位置选钟 2号
    S.staffsWork(S.NOR, 1)
    S.staffsWait(1)
    S.reportStaffs()
    S.staffsWork(S.NOR, 2)
    S.reportStaffs()
    S.staffsWait(2)
    S.staffsWork(S.SEL, 2)
    S.reportStaffs()
    S.staffsWork(S.NOR, 3)
    S.staffsWait(3)
    S.reportStaffs()
    S.staffsWork(S.SEL, 3)
    S.reportStaffs()


    # 重建测试环境
    print()
    print()
    print()
    S.clear()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9,)
    S.reportStaffs()
    S.staffsWait(1,2,3,4,5,6,7,8,9)
    # 测试 无选钟情况下的点钟.
    S.staffsWork(S.NOR, 1,2,3)
    S.staffsWork(S.NAMED, 4)
    S.reportStaffs()

    # 重建测试环境
    print()
    print()
    print()
    S.clear()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9,)
    S.reportStaffs()
    S.staffsWait(1,2,3,4,5,6,7,8,9)
    # 测试 有选钟情况下的点钟.
    S.staffsWork(S.SEL, 1,2,3)
    S.reportStaffs()
    S.staffsWork(S.NAMED, 4)
    S.reportStaffs()
    # 测试存入文件
    S.save("test.qpc")
    S.load("test.qpc")
    # 此时 1,2,3,4 处于第3次工作队列.
    #      5 至 9 都留在第2次工作队列处于 等待状态
    # 测试 reportStaffs()
    # 测试 上述(选钟插在正常之间)情形之后, 正常工作
    # 测试 staffWork(Id, wType)
    # 6号 插在 5号 前面. 通过!
    # 测试 4空 6,5, 正常工作状态
    # !!! 有问题, 第三次的 nPos 没有恢复为1
    # @@@ 问题修复
    # 因为2号为选钟上班. 逻辑错误.
    # 测试 1N, 2N, 3N, 4N, 6S, 5S 之后 正常工作的情况
    # 全部进入等待状态
