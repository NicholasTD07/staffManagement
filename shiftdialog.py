#!/usr/bin/python3
# File Info :
#   员工分组对话框


# PyQt #
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# 调用 #
import staffdata


class ShiftDialog(QDialog) :


#{{{ # 初始化员工换班对话框 #
    def __init__(self, staffs, parent=None) :
        # 初始化 #
        super(ShiftDialog, self).__init__(parent)
        self.workGrpChanged = False

        # 获取员工信息 #
        self.staffs = staffs
        self.workTypes = staffs.workTypes
        self.groups = staffs.getGroups()
        self.getWorkGroup = staffs.getWorkGroup
        workGroupNum = self.getWorkGroup()
        self.workGroupNum = workGroupNum
        if workGroupNum is None :
            QMessageBox.warning(self,
                    "未设置上班分组.",
                    "当前显示的上班分组为第一个员工分组,"
                    "并不是上班分组.")
            workGroupNum = 0
        self.workGroup = self.groups[workGroupNum]
        self.lenGroups = len(self.groups)
        self.workStaffs = []

        # 设置界面 #
        self.setupUi()

        # 更新内容 #
        self.updateWorkTable()
        self.updateStandbyTable()

        #---- 自定义信号 ----#

        # 点击员工 #
        self.connect(self.workTable, SIGNAL("cellClicked(int, int)"),
                self.on_workTableItem_clicked)
                #lambda : print("点击按键"))
        self.connect(self.shiftGrpSpinBox, SIGNAL("valueChanged(int)"),
                self.on_shiftGrpSpinBox_valueChanged)
                #lambda : print("点击按键"))

        self.connect(self.shiftGroupButton, SIGNAL("clicked()"),
                self.on_shiftGroupButton_clicked)

        # 链接信号 #
        self.connect(self.buttonBox, SIGNAL("accepted()"),
                        self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"),
                        self.reject)
#}}}

    #---- 重定义函数 ----#

    def accept(self) :
        QDialog.accept(self)

    def reject(self) :
        if self.workGrpChanged :
            QDialog.accept(self)
            print("Changed, accepting.")
        else :
            QDialog.reject(self)
            print("not changed, rejecting.")

    #---- 自定义槽 ----#

    #{{{ # 点击表格 #
    def on_workTableItem_clicked(self) :
        # 初始化局部变量 #
        workTable = self.workTable
        staffWait = self.staffs.staffWait
        # 获取员工信息 #
        item = workTable.currentItem()
        if item is None :
            return
        Id = int(item.data(Qt.UserRole))
        # 进入等待状态 #
        if staffWait(Id) :
            self.workStaffs.remove(Id)
        item.setBackground( QColor(0,255,0) )

    def on_shiftGrpSpinBox_valueChanged(self) :
        # 初始化局部变量 #
        spinBox = self.shiftGrpSpinBox
        value = spinBox.value()
        lenGroups = self.lenGroups
        # 判断数据合法性 #
        if value > lenGroups :
            QMessageBox.warning(self,
                    "设置分组",
                    "超出当前最大分组数.自动设置为当前最大值")
            spinBox.setValue(lenGroups)
        self.updateStandbyTable()
    #}}}

    #{{{ # 点击换班按钮 #
    def on_shiftGroupButton_clicked(self) :
        # 初始化局部变量 #
        standbyGrpNum = self.shiftGrpSpinBox.value() - 1
        if standbyGrpNum == self.workGroupNum :
            return
        workStaffs = self.workStaffs
        setWorkGroup = self.staffs.setWorkGroup
        shiftStaff = self.staffs.shiftStaff
        # 检查员工状态 #
        if workStaffs :
            QMessageBox.warning(self,
                    "上班分组员工状态错误",
                    "员工工号为 {} 的员工依然处于工作状态."
                    "请转换状态后再换班."\
                            .format(workStaffs))
            return
        # 更新上班分组号 #
        shiftStaff(standbyGrpNum)
        setWorkGroup(standbyGrpNum)
        self.staffs.reportStaffs()
        # 更新界面 #
        workGroupNum = self.getWorkGroup()
        if workGroupNum is None :
            workGroupNum = 0
        self.workGroup = self.groups[workGroupNum]
        self.workGroupLabel.setText("上班分组: {}"\
                .format((workGroupNum + 1)))
        self.updateWorkTable()
        QMessageBox.information(self,
               "员工换班",
               "员工换班成功!")
        self.workGrpChanged = True
        self.workGroupNum = standbyGrpNum
    #}}}

    #{{{ #---- 设置界面 ----#
    def setupUi(self) :
        #-- 添加组件 --#
        # 标签 #
        workGroupNum = self.getWorkGroup()
        if workGroupNum is None :
            self.workGroupLabel = QLabel("第一分组", self)
        else :
            self.workGroupLabel = QLabel("上班分组: {}"\
                    .format(workGroupNum + 1), self)
        self.shiftGroupLabel = QLabel("换班分组:", self)
        self.helpLabel = QLabel(
                "说明:"
                "\n上班分组所有员工必须处于等待状态"
                "才可换班."
                "(红色员工正在上班,点击员工即可进入等待状态.)", self) 

        # 数字框 #
        shiftGrpSpinBox = QSpinBox(self)
        shiftGrpSpinBox.setRange(1, len(self.groups))
        shiftGrpSpinBox.setValue(1)
        self.shiftGrpSpinBox = shiftGrpSpinBox

        # 按键 #
        self.shiftGroupButton = QPushButton()
        self.shiftGroupButton.setText("换班")

        # 按键组 #
        buttonBox = QDialogButtonBox(self)
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(
                QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).setText("确认")
        self.buttonBox = buttonBox

        # 表格 #
        self.workTable = QTableWidget(self)
        self.standbyTable = QTableWidget(self)

        #-- 组织结构 --#

        # 上(横向) #
        HBoxLayout1  = QHBoxLayout()
        HBoxLayout1.addWidget(self.workGroupLabel)
        HBoxLayout1.addStretch()
        HBoxLayout2  = QHBoxLayout()
        HBoxLayout2.addWidget(self.shiftGroupLabel)
        HBoxLayout2.addWidget(self.shiftGrpSpinBox)
        HBoxLayout2.addWidget(self.shiftGroupButton)

        # 挂入对话框 #
        self.HBoxLayout1 = HBoxLayout1
        self.HBoxLayout2 = HBoxLayout2

        # 对话框结构 #
        gridLayout = QGridLayout()
        addWidget = gridLayout.addWidget
        gridLayout.addLayout(self.HBoxLayout1, 0, 1, 1, 2)
        gridLayout.addLayout(self.HBoxLayout2, 0, 2, 1, 2)
        addWidget(self.workTable, 2, 1, 1, 1)
        addWidget(self.standbyTable, 2, 2, 1, 1)
        addWidget(self.helpLabel, 3, 1, 1, 2)
        addWidget(self.buttonBox,  4, 2, 1, 1)
        self.gridLayout = gridLayout

        # 设置框体属性 #
        self.setLayout(self.gridLayout)
        self.resize(540, 330)
        self.setWindowTitle("换班")
    #}}}

    #---- 更新表格 ----#

    #{{{ # 上班表格 #
    def updateWorkTable(self) :
        # 初始化局部变量 #
        workColor = QColor(255,0,0)
        waitColor = QColor(0, 255, 0)
        i = 0
        columnCount = 10
        workTypes = self.workTypes
        workGroup = self.workGroup
        workTable = self.workTable
        lenWorkGrp = len(workGroup)
        workStaffs = self.workStaffs
        if workStaffs :
            print("奇怪的错误.")
        addWorkStaff = workStaffs.append
        getStaff = self.staffs.getStaff
        # 清除所有内容 #
        workTable.clear()
        workTable.setRowCount(int(lenWorkGrp/columnCount) + 1)
        workTable.setColumnCount(columnCount)
        # 更新表格内容 #
        while i < lenWorkGrp :
            Id = workGroup[i]
            wType = getStaff(Id).wType
            item = QTableWidgetItem(str(Id))
            if wType in workTypes :
                item.setBackground(workColor)
                addWorkStaff(Id)
            else :
                item.setBackground(waitColor)
            item.setData(Qt.UserRole, int(Id))
            item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            workTable.setItem(i//columnCount, i%columnCount, item)
            i += 1
        workTable.resizeColumnsToContents()
    #}}}

    #{{{ # 换班表格 #
    def updateStandbyTable(self) :
        # 初始化局部变量 #
        i = 0
        columnCount = 10
        groups = self.groups
        spinBox = self.shiftGrpSpinBox
        workTypes = self.workTypes
        standbyTable = self.standbyTable
        standbyGrp = self.groups[spinBox.value()-1]
        lenStandby = len(standbyGrp)
        # 清除所有内容 #
        standbyTable.clear()
        standbyTable.setRowCount(int(lenStandby/columnCount) + 1)
        standbyTable.setColumnCount(columnCount)
        # 更新表格内容 #
        while i < lenStandby :
            Id = standbyGrp[i]
            item = QTableWidgetItem(str(Id))
            item.setData(Qt.UserRole, int(Id))
            item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            standbyTable.setItem(i//columnCount, i%columnCount, item)
            i += 1
        standbyTable.resizeColumnsToContents()
    #}}}

if __name__ == "__main__" :
    import sys
    app = QApplication(sys.argv)

    S = staffdata.StaffContainer()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
    S.groupStaff(1,1)
    S.groupStaff(2,1)
    S.groupStaff(3,1)
    S.shiftStaff(1)
    S.staffsWork(S.NOR, 1,2,3)

    form = ShiftDialog(S)
    form.show()
    sys.exit(app.exec_())
