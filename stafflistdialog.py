#!/usr/bin/python3
# File Info :
#   查看员工队列对话框

#    Copyright 2012 Nicholas Tian

#    This file is part of Staff Management Project.
#
#    Staff Management Project is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Straff Management Project is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Straff Management Project.  If not, see <http://www.gnu.org/licenses/>.


# PyQt #
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# 调用 #
import staffdata
import updatestaffdialog


class StaffListDialog(QDialog) :


    WORK, WAIT = range(2)

    #{{{ # 初始化查看员工对话框 #
    def __init__(self, staffs=None, parent=None) :
        # 初始化 #
        super(StaffListDialog, self).__init__(parent)
        # 判断: 是否输入员工信息 #
        if staffs is None :
            QMessageBox.warning(self,
                    "查看员工队列",
                    "当前队列为空,  自动退出.")
            return
        self.staffs = staffs
        self.setupUi()

        # 载入: 员工, 员工序列
        self.workSeqs = staffs.getWorkSeq()
        self.workTypes = staffs.workTypes

        # 生成: 所有员工表, 工作员工表, 等待员工表
        self.populateAll()

        #{{{ #---- 自定义信号 ----#
        self.connect(self.IdSpinBox, SIGNAL("valueChanged(int)"),
                self.on_IdSpinBox_valueChanged)
                #lambda : print("点击按键"))
        self.connect(self.staffTable, SIGNAL("cellDoubleClicked(int,int)"),
                self.on_staffTable_cellDoubleClicked)
                #lambda : print("点击按键"))
        #}}}
    #}}}

    #{{{ # 设置界面 #
    def setupUi(self) :
        #-- 添加组件 --#

        # 标签 #
        self.IdLabel = QLabel("员工工号:", self)
        self.staffTableLabel = QLabel("查看员工:", self)
        self.helpLabel = QLabel(
                "提示: 可双击更改员工信息.本框中直接修改无效.")

        # 数字框 #
        IdSpinBox = QSpinBox(self)
        IdSpinBox.setRange(0, len(self.staffs))
        IdSpinBox.setValue(1)
        self.IdSpinBox = IdSpinBox

        # 按键组 #
        buttonBox = QDialogButtonBox(self)
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons( QDialogButtonBox.Close)
        buttonBox.button(QDialogButtonBox.Close).setText("关闭")
        self.buttonBox = buttonBox

        # 表格 #
        self.staffTable = QTableWidget(self)

        #-- 组织结构 --#

        # 上(横向) #
        HBoxLayout  = QHBoxLayout()
        HBoxLayout.addWidget(self.staffTableLabel)
        HBoxLayout.addStretch()
        HBoxLayout.addWidget(self.IdLabel)
        HBoxLayout.addWidget(IdSpinBox)
        # 挂入对话框 #
        self.HBoxLayout = HBoxLayout

        # 对话框结构 #
        gridLayout = QGridLayout()
        gridLayout.addLayout(HBoxLayout, 0, 0, 1, 2)
        gridLayout.addWidget(self.staffTable, 1,0, 1, 2)
        gridLayout.addWidget(self.helpLabel, 2, 0, 1, 1)
        gridLayout.addWidget(buttonBox, 2, 1, 1, 1,)
        # 挂入对话框 #
        self.gridLayout = gridLayout

        # 设置框属性 #
        self.resize(600, 370)
        self.setMinimumSize(600, 370)
        self.setLayout(gridLayout)
        sizePolicy = QSizePolicy(
                QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        self.setSizePolicy(sizePolicy)
        self.setWindowTitle("查看员工")
    #}}}

    #{{{ # 重定义: 按键事件 #
    def keyPressEvent(self, event) :
        if event.key() == Qt.Key_Enter :
            event.ignore()
        elif event.key() == Qt.Key_Escape :
            QDialog.reject(self)
        else :
            QWidget.keyPressEvent(self, event)
    #}}}

    #{{{ #---- 定义槽 ----#

    # 值改变: 员工工号输入框 #
    def on_IdSpinBox_valueChanged(self) :
        if Id not in self.staffs.getStaffs() :
            QMessageBox.warning(self,
                    "员工工号错误",
                    "没有此工号."
                    "\n请查询后重新输入.")
            return
        # 定位: 所有员工表
        self.staffTable.setCurrentCell(0, Id - 1)

    # 双击: 所有员工表 #
    def on_staffTable_cellDoubleClicked(self) :
        column = self.staffTable.currentColumn()
        item = self.staffTable.item(0, column)
        self.updateStaff(item, column)
    #}}}

    #{{{ #---- 辅助函数 ----#
    
    # 获得员工, 并弹出更新信息窗口 #
    def updateStaff(self, item, column) :
        # 1. 判断: 该位置是否有员工
        if item is None :
            return
        else :
            Id = int(item.data(Qt.UserRole))
        # 2. 获得: 员工实例
        staff = self.staffs.getStaff(Id)
        # 3. 判断: 员工是否存在
        if staff :
            form = updatestaffdialog.UpdateStaffDialog(
                        self.staffs, staff, self)
        else :
            return
        # 3. 弹出窗口并更新表格
        if form.exec_() :
            wTime = staff.wTime
            wType = staff.wType
            staffs = self.staffs
            workSeqs = self.workSeqs
            nSeq = workSeqs[wTime].nSeq
            setItem = self.staffTable.setItem
            staff = self.staffs.getStaff(Id)
            if wType == staffs.IDLE :
                waitPos = None
                workPos = None
            elif wType in staffs.workTypes :
                waitPos = None
                workPos = nSeq.index(staff)
            else :
                waitPos = nSeq.index(staff)
                workPos = None
            item = QTableWidgetItem(str(staff.Id))
            item.setData(Qt.UserRole, int(Id))
            setItem(0, column, item)
            setItem(1, column,
                   QTableWidgetItem(str(staff.name)))
            setItem(2, column,
                   QTableWidgetItem(str(staff.gender)))
            setItem(3, column,
                   QTableWidgetItem(str(staff.wTime)))
            setItem(4, column,
                    QTableWidgetItem(str(staff.wType)))
            # 等待位置 #
            setItem(5, column,
                    QTableWidgetItem(
                        "" if waitPos is None else str(waitPos)))
            # 工作位置 #
            setItem(6, column,
                    QTableWidgetItem(
                        "" if workPos is None else str(workPos)))
            item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            # 调整: 列的宽度
            self.staffTable.resizeColumnsToContents()
    #}}}

    #{{{ #---- 生成表格 ----#

    # 生成: 所有员工表
    def populateAll(self) :
        # 初始化局部变量 #
        staffs = self.staffs
        workSeqs = self.workSeqs
        IDs = staffs.getIDs()
        getStaff = staffs.getStaff
        IDLE = staffs.IDLE
        WAIT = staffs.WAIT
        workTypes = staffs.workTypes
        staffTable = self.staffTable
        setItem = staffTable.setItem
        # 表头 #
        heads = [ str(i) for i in IDs ]
        vHeads = [ "员工工号", "姓名", "性别", "工作次数",
                "工作类型", "等待位置", "工作位置" ]
        # 清除: 已有内容
        staffTable.clear()
        # 初始化: 设置 
        staffTable.setSortingEnabled(False)
        staffTable.setRowCount(len(vHeads))
        staffTable.setColumnCount(len(heads))
        # 设置: 表头
        staffTable.setVerticalHeaderLabels(vHeads)
        # 设置: 内容
        for column, Id in enumerate(IDs) :
            # 初始化循环内部变量 #
            staff = getStaff(Id)
            wTime = staff.wTime
            wType = staff.wType
            nSeq = workSeqs[wTime].nSeq
            if wType == IDLE :
                waitPos = None
                workPos = None
            elif wType in workTypes :
                waitPos = None
                workPos = nSeq.index(staff)
            else :
                waitPos = nSeq.index(staff)
                workPos = None
            item = QTableWidgetItem(str(staff.Id))
            item.setData(Qt.UserRole, int(Id))
            setItem(0, column, item)
            setItem(1, column,
                   QTableWidgetItem(str(staff.name)))
            setItem(2, column,
                   QTableWidgetItem(str(staff.gender)))
            setItem(3, column,
                   QTableWidgetItem(str(staff.wTime)))
            setItem(4, column,
                    QTableWidgetItem(str(staff.wType)))
            # 等待位置 #
            setItem(5, column,
                    QTableWidgetItem(
                        "" if waitPos is None else str(waitPos)))
            # 工作位置 #
            setItem(6, column,
                    QTableWidgetItem(
                        "" if workPos is None else str(workPos)))
            item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        # 调整: 列的宽度
        staffTable.resizeColumnsToContents()
    #}}}

if __name__ == '__main__' :
    import sys

    S = staffdata.StaffContainer()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
    #S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12,13,14,15)
    #S.staffsWork(S.NOR,1, 2, 3, 4, 6, 8, 9)
    #S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)

    app = QApplication(sys.argv)
    form = StaffListDialog(S)
    form.show()
    sys.exit(app.exec_())
