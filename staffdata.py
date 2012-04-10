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
        self.sPos = [1]
        self.selected = False
        self.nSeq = []


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

    # 基本操作 #

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

        # 1. 获得员工基本信息
        staff = self.__staffs[Id]
        wTime = staff.wTime
        wType = staff.wType

        # 2. 判断员工当前状态是否为等待状态
        if wType is not self.WAIT :
            self.log("\t\t!!!----失败: 员工当前状态错误----!!!")
            raise Exception

        # 3. 使员工脱离工作队列
        pos = self.__workSeqs[wTime].nSeq.index(staff)
        self.__workSeqs[wTime].nSeq.remove(staff)
        self.__workSeqs[wTime].nSeq.insert(pos, None)
        self.log("\t\t员工脱离第{}次工作队列.".format(wTime))

        # 4. 更新工作次数
        staff.wTime += 1
        wTime = staff.wTime
        self.updateMaxSeq(wTime)

        # 5. 更新状态
        staff.wType = self.NOR
        staff.sType = self.NOR
        self.log("\t\t员工当前工作次数: {}, 工作状态: {}"\
            .format(staff.wTime, staff.wType))

        # 6. 员工按照序列正常工作序号, 进入序列
        # 6.1 取得当前序列正常工作序号
        nPos = ( max(self.__workSeqs[wTime].nPos) + 1 )
        # 6.2 检查当前序列长度
        checked = False
        while len(self.__workSeqs[wTime].nSeq) <= nPos :
            self.__workSeqs[wTime].nSeq.append(None)
            if not checked :
                self.log("\t\t当前工作序列长度小于工作序号, 自动增加中.")
                checked = True
        # 6.3 判断工作位置状态
        inPos = self.__workSeqs[wTime].nSeq[nPos]
        if inPos is None :
            self.__workSeqs[wTime].nSeq[nPos] = staff
            self.log("\t\t员工工作位置为空, 正常上班.")
        elif isinstance(inPos, Staff) and inPos.wType is self.SEL :
            self.__workSeqs[wTime].nSeq.insert(nPos, staff)
            self.log("\t\t员工工作位置非空为选钟员工, 插队上班.")
        else :
            self.log("\t\t!!!----错误: 插入员工时出现未知错误.----!!!")
            raise Exception

        # 7. 更新队列工作序号
        self.__workSeqs[wTime].nPos.append(nPos)
        
        # 8. 加入变动员工组
        self.__modStaffs.add(staff)

        # 9. 操作完成, 设置文件改动
        self.log("\t\t@@@---- 成功: 员工正常上班操作 ----@@@")
        self.__dirty = True

    def selWork(self, Id) :
        self.log("\t\t{}号员工选钟上班工作:".format(Id))

        # 1. 获得员工基本信息
        staff = self.__staffs[Id]
        wTime = staff.wTime
        wType = staff.wType

        # 2. 判断员工当前状态是否为等待状态
        if wType is not self.WAIT :
            self.log("\t\t!!!----失败: 员工当前状态错误----!!!")
            raise Exception

        # 3. 提取当前工作序号, 使员工脱离工作队列
        # 3.1 判断员工工作状态
        pos = self.__workSeqs[wTime].nSeq.index(staff)
        self.__workSeqs[wTime].nSeq.remove(staff)
        self.__workSeqs[wTime].nSeq.insert(pos, None)
        self.log("\t\t员工脱离第{}次工作队列, 工作序号: {}."\
            .format(wTime, pos))

        # 4. 更新工作次数
        staff.wTime += 1
        wTime = staff.wTime
        self.updateMaxSeq(wTime)

        # 5. 更新状态
        staff.wType = self.SEL
        staff.sType = self.SEL
        self.log("\t\t员工当前工作次数: {}, 工作状态: {}"\
            .format(staff.wTime, staff.wType))

        # 6. 员工按照上次序列工作序号, 进入序列
        # 6.1 已取得当前工作序号
        # 6.2 检查当前序列长度
        checked = False
        while len(self.__workSeqs[wTime].nSeq) <= pos :
            self.__workSeqs[wTime].nSeq.append(None)
            if not checked :
                self.log("\t\t当前工作序列长度小于工作序号, 自动增加中.")
                checked = True
        # 6.3 判断工作位置状态, 插入队伍
        inPos = self.__workSeqs[wTime].nSeq[pos]
        if inPos is None :
            self.__workSeqs[wTime].nSeq[pos] = staff
        else :
            self.__workSeqs[wTime].nSeq.insert(pos, staff)

        # 7. 更新 selected 状态, 更新 sPos
        if not self.__workSeqs[wTime].selected :
            self.__workSeqs[wTime].selected = True
        sPos = max(self.__workSeqs[wTime].sPos)
        if pos + 1 > sPos :
            self.__workSeqs[wTime].sPos.append(pos + 1)
        elif pos < sPos :
            self.__workSeqs[wTime].sPos.append(sPos + 1)

        # 8. 判断是否需要更新 nPos
        nPos = self.__workSeqs[wTime].nPos
        #nPos = max(self.__workSeqs[wTime].nPos)
        if pos < max(nPos) :
            if pos in nPos :
                self.__workSeqs[wTime].nPos.remove( pos )
            self.__workSeqs[wTime].nPos.append(max(nPos)+1)

        # 9. 加入变动员工组
        self.__modStaffs.add(staff)
        
        # 10. 操作完成, 设置文件改动
        self.log("\t\t@@@---- 成功: 员工选钟上班操作 ----@@@")
        self.__dirty = True

    def namedWork(self, Id) :
        self.log("\t\t{}号员工点钟上班工作:".format(Id))

        # 1. 获得员工基本信息
        staff = self.__staffs[Id]
        wTime = staff.wTime
        wType = staff.wType

        # 2. 判断员工当前状态是否为等待状态
        if wType is not self.WAIT :
            self.log("\t\t!!!----失败: 员工当前状态错误----!!!")
            raise Exception

        # 3. 使员工脱离工作队列
        pos = self.__workSeqs[wTime].nSeq.index(staff)
        self.__workSeqs[wTime].nSeq.remove(staff)
        self.__workSeqs[wTime].nSeq.insert(pos, None)
        self.log("\t\t员工脱离第{}次工作队列.".format(wTime))

        # 4. 更新工作次数
        staff.wTime += 1
        wTime = staff.wTime
        self.updateMaxSeq(wTime)

        # 5. 更新状态
        staff.wType = self.NAMED
        self.log("\t\t员工当前工作次数: {}, 工作状态: {}"\
            .format(staff.wTime, staff.wType))

        # 6. 员工按照序列正常工作序号进入序列
        # 6.1 取得当前序列正常工作序号
        nPos = ( max(self.__workSeqs[wTime].nPos) + 1 )
        sPos = ( max(self.__workSeqs[wTime].sPos) + 1 )
        # 6.2 判断 checked 状态
        if self.__workSeqs[wTime].selected : # 有选钟, 放在队列末尾
            # 6.3 检查序列长度
            checked = False
            while len(self.__workSeqs[wTime].nSeq) <= sPos :
                self.__workSeqs[wTime].nSeq.append(None)
                if not checked :
                    self.log("\t\t当前工作序列长度小于工作序号, 自动增加中.")
                    checked = True
            if self.__workSeqs[wTime].\
            nSeq[sPos-1].wType == self.SEL :
                inPos = self.__workSeqs[wTime].nSeq[sPos]
                if inPos is None :
                    self.log("\t\t员工正常上点钟!")
                    self.__workSeqs[wTime].\
                    nSeq[sPos] = staff
                    self.__workSeqs[wTime].\
                    sPos.append(sPos + 1)
                    staff.sType = self.SEL
                else :
                    self.log("员工工作位置非空.退出.")
                    raise Exception
            else :
                self.log("员工上一个位置并非SEL.退出.")
                raise Exception
        else :  # 无选钟插在中间
            # 6.3 检查序列长度
            checked = False
            while len(self.__workSeqs[wTime].nSeq) <= nPos :
                self.__workSeqs[wTime].nSeq.append(None)
                if not checked :
                    self.log("\t\t当前工作序列长度小于工作序号, 自动增加中.")
                    checked = True
            inPos = self.__workSeqs[wTime].nSeq[nPos-1]
            if inPos is None or (isinstance(inPos, Staff) and inPos.wType == self.NOR) :
                inPos = self.__workSeqs[wTime].nSeq[nPos]
                if inPos is None :
                    self.log("\t\t员工正常上点钟!")
                    self.__workSeqs[wTime].\
                    nSeq[nPos] = staff
                    self.__workSeqs[wTime].\
                    nPos.append(nPos + 1)
                    staff.sType = self.NOR
                else :
                    self.log("员工工作位置异常.退出.")
                    raise Exception
            else :
                self.log("员工上一个位置非空或者不是NOR.退出.")
                raise Exception

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

        # 6.将员工加入 变动员工组
        self.__modStaffs.add(Id)

        # 7.操作完成, 设置 dirty
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
        elif wType is self.IDLE :
            staff.wType = self.WAIT
            self.__workSeqs[0].nSeq.append(staff)

        # 3. 更新 nPos, sPos
        if sType is self.NOR :
            self.__workSeqs[wTime].nPos.remove( pos )
        elif sType is self.SEL :
            self.__workSeqs[wTime].sPos.remove( pos + 1 )
        else :
            self.log("\t@@@--员工处于空闲态, 无 pos, 无操作.")
            
        # 4. 加入变动员工组
        self.__modStaffs.add(staff)

        # 5. 操作成功
        self.log("\t@@@----成功: 员工等待操作----@@@")
        self.__dirty = True

    def staffWork(self, Id, wType=NOR) :
        self.log("\t{}员工{}工作操作:".format(Id, wType))

        if wType is self.NOR :
            self.norWork(Id)
        elif wType is self.SEL :
            self.selWork(Id)
        elif wType is self.NAMED :
            self.namedWork(Id)
        else :
            raise Exception

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
            print("第{}次时间序列, nPos = {}, sPos = {}, {}选钟工作员工.".format(wTime, nPos, sPos, "有" if selected else "没有"))
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
    
#    S = StaffContainer()
#    S.log("\nAGAIN")
#
#
#    startTime = time()
#    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9)
#    createTime = time()
#    S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
#    #S.reportStaffs()
#    S.staffsWork(S.NOR, 1, 2, 3, 4, 5, 6, 7, 8, 9)
#    staffWorkTime = time()
#
#    S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
#    S.staffsWork(S.SEL, 1, 2, 3, 4, 5, 6, 7, 8, 9)
#    S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
#    staffWork2Time = time()
#    #S.reportStaffs()
#    endTime = time()
#    print("""创建员工时间 {0} \n
#员工第一次工作时间 {1}\n员工第二次工作时间 {2}
#报告时间 {3}"""\
#        .format((createTime - startTime),
#            (staffWorkTime - createTime),
#            (staffWork2Time - staffWorkTime),
#            (endTime - staffWorkTime)))
#    print("员工工号: {}".format(S.getIDs()))
#
#    S.staffsWork(S.NOR, 4, 5, 6)
#    S.staffsWork(S.NAMED, 7, 8)
#    S.getStaffs()[1].tell()
#    S.staffsWork(S.SEL, 1, 2, 3)
#    S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
#    S.staffsWork(S.NAMED, 5, 6)
#    S.staffsWork(S.SEL, 9)
#    #S.reportStaffs()
#    S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
#    #S.reportStaffs()
#
#    S.save("/home/thedevil/test.qpc")
#    S.load("/home/thedevil/test.qpc")

    S = StaffContainer()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9)
    # 测试 等待操作
    S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    # 测试 全部正常工作
    S.staffsWork(S.NOR, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    # 测试 全部选钟工作
    S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    S.staffsWork(S.SEL, 1, 2, 3, 4, 5, 6, 7, 8, 9)
    # 测试 1N, 3N, 4N, 2S(应在 1,3 之间)
    S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    S.staffsWork(S.NOR, 1, 3, 4)
    S.reportStaffs()
    S.staffsWork(S.SEL, 2)
    # 此时 1,2,3,4 处于第3次工作队列.
    #      5 至 9 都留在第2次工作队列处于 等待状态
    # 测试 reportStaffs()
    S.reportStaffs()
    # 测试 上述(选钟插在正常之间)情形之后, 正常工作
    #S.staffsWork(S.NOR, 5)
    # 测试 staffWork(Id, wType)
    S.staffWork(5, S.NOR)
    S.reportStaffs()
    # 测试 多个员工同一位置选钟 2号
    S.staffWait(5) # 5 在第3次时间队列
    S.staffWork(5, S.SEL)
    S.staffWork(6) # 6 在第2次时间队列
    S.reportStaffs()
    S.staffWait(6)
    S.staffWork(6, S.SEL)
    S.reportStaffs()
    # 6号 插在 5号 前面. 通过!
    # 测试 4空 6,5, 正常工作状态
    S.staffsWait(1,2,3,4)
    # !!! 有问题, 第三次的 nPos 没有恢复为1
    # @@@ 问题修复
    S.reportStaffs()
    # 因为2号为选钟上班. 逻辑错误.
    S.staffsWork(S.NOR, 1, 2, 3, 4)
    S.reportStaffs() # 测试通过
    # 测试 1N, 2N, 3N, 4N, 6S, 5S 之后 正常工作的情况
    S.staffsWork(S.NOR, 7,8,9)
    S.reportStaffs()
    S.staffsWait(7,8,9)
    S.reportStaffs()
    S.staffsWork(S.NOR, 7,8,9)
    S.reportStaffs()
