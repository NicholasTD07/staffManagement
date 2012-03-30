#!/usr/bin/python3
# File Info :
#   查看员工队列对话框

# 系统 #
import sys

# PyQt #
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# 调用 #
import staffdata
import ui_stafflistdialog
###import updatestaffdialog

__version__ = "0.3.0"

class StaffListDialog(QDialog,
            ui_stafflistdialog.Ui_StaffListDialog) :

    WORK, WAIT = range(2)

    def __init__(self, staffs=None, parent=None) :
        # 初始化 #
        super(StaffListDialog, self).__init__(parent)
        self.setupUi(self)

        # 判断: 是否输入员工信息 #
        if staffs is None :
            QMessageBox.warning(self,
                    "查看员工队列",
                    "当前队列为空,  自动退出.")
            return
        self.staffs = staffs

        # 生成: 所有员工表, 工作员工表, 等待员工表
        self.populateAll()
        self.populate(self.WORK)
        self.populate(self.WAIT)
        self.buttonBox.button(QDialogButtonBox.Close).setText(
                "退出")

    # 重定义: 按键事件 #
    def keyPressEvent(self, event) :
        if event.key() == Qt.Key_Enter :
            event.ignore()
        elif event.key() == Qt.Key_Escape :
            QDialog.reject(self)
        else :
            QWidget.keyPressEvent(self, event)

    #---- 定义槽 ----#

    # 值改变: 员工工号输入框 #
    @pyqtSignature("int")
    def on_IdSpinBox_valueChanged(self, Id) :
        if Id not in self.staffs.getStaffs() :
            QMessageBox.warning(self,
                    "员工工号错误",
                    "没有此工号."
                    "\n请查询后重新输入.")
        self.findCell(self.allTable, 0, Id-1)
        self.findCell(self.workTable, 0, Id-1)
        self.findCell(self.waitTable, 0, Id-1)

    # 双击: 所有员工表 #
    def on_allTabel_cellDoubleClicked(self, row, column) :
        item = self.allTable.item(0, column)
        # 1. 判断: 该位置是否有员工
        if item is None :
            return
        else :
            Id = int(item.data(Qt.UserRole))
        # 2. 获得: 员工实例
        staff = self.staffs.getStaff(Id)
        # 判断: 员工是否存在
        if staff is not None :
            form = updatestaffdialog.UpdateStaffDialog(
                        self.staffs, staff, self)
        else :
            return
        # 3. 弹出窗口并更新表格
        if form.exec_() :
            self.populateAll()
            self.populate(self.WORK)
            self.populate(self.WAIT)

    # 双击: 工作员工表 #
    def on_workTable_cellDoubleClicked(self, row, column) :
        self.cellDoubleClicked(self.WORK, row, column)

    # 双击: 等待员工表
    def on_waitTable_cellDoubleClicked(self, row, column) :
        self.cellDoubleClicked(self.WAIT, row, column)

    #---- 辅助函数 ----#

    def cellDoubleClicked(self, seq, row, column) :
        if seq is self.WORK :
            item = self.workTable.item(row, column)
        elif seq is self.WAIT :
            item = self.waitTable.item(row, column)
        # 1. 判断: 该位置是否有员工
        if item is None :
            return
        else :
            Id = int(item.data(Qt.UserRole))
        # 2. 获得: 员工实例
        staff = self.staffs.getStaff(Id)
        # 3. 判断: 员工是否存在
        if staff is not None :
            form = updatestaffdialog.UpdateStaffDialog(
                        self.staffs, staff, self)
        else :
            return
        # 3. 弹出窗口并更新表格
        if form.exec_() :
            self.populateAll()
            self.populate(self.WORK)
            self.populate(self.WAIT)
        
    def findCell(self, table=None, row=0, column=0) :
        if table is not None :
            table.setCurrentCell(row, column)

    #---- 生成表格 ----#

    # 生成: 所有员工表
    def populateAll(self) :
        IDs = self.staffs.getIDs()
        # 生成: 表头
        heads = [str(i) for i in IDs]
        vHeads = ["员工工号", "姓名", "性别",
                        "工作次数", "等待位置", "工作位置"]
        # 清除: 已有内容
        self.allTable.clear()
        # 初始化: 设置 
        self.allTable.setSortingEnabled(False)
        self.allTable.setRowCount(len(vHeads))
        self.allTable.setColumnCount(len(heads))
        # 设置: 表头
        self.allTable.setVerticalHeaderLabels(vHeads)
        # 设置: 内容
        for column, Id in enumerate(IDs) :
            staff = self.staffs.getStaff(Id)
            item = QTableWidgetItem(str(staff.Id))
            item.setData(Qt.UserRole, int(Id))
            self.allTable.setItem(0, column, item)
            self.allTable.setItem(1, column,
                    QTableWidgetItem(str(staff.name)))
            self.allTable.setItem(2, column,
                    QTableWidgetItem(str(staff.gender)))
            self.allTable.setItem(3, column,
                    QTableWidgetItem(str(staff.wTime)))
            self.allTable.setItem(4, column,
                    QTableWidgetItem(
                    "" if staff.waitPos is None else
                        str(staff.waitPos)))
            self.allTable.setItem(5, column,
                    QTableWidgetItem(
                    "" if staff.workPos is None else
                        str(staff.workPos)))
            item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        # 调整: 列的宽度
        self.allTable.resizeColumnsToContents()
    
    # 生成: 工作表 或者 等待表
    def populate(self, seq) :
        workSeqs = self.staffs.getWorkSeq()
        maxTime = self.staffs.getMaxTime()
        # 选择: 最大值 及 (工作表 或 等待表)
        if seq is self.WORK :
            maxPos = self.staffs.getMaxWorkPos()
            table = self.workTable
        elif seq is self.WAIT :
            maxPos = self.staffs.getMaxWaitPos()
            table = self.waitTable
        else :
            return 
        # 生成: 表头
        vHeads = range( maxTime + 1 )
        heads = range( 1, maxPos + 1 )
        heads = [ "序号:{}".format(head) for head in heads ]
        # 清除: 已有内容
        table.clear()
        # 初始化: 设置
        table.setSortingEnabled(False)
        table.setRowCount(len(vHeads))
        table.setColumnCount(len(heads))
        # 设置: 表头
        table.setHorizontalHeaderLabels(heads)
        table.setVerticalHeaderLabels(
                [ "工作次数".format(i) for i in vHeads])
        # 设置: 内容
        for row, workSeq in enumerate(workSeqs) :
            for (pos, Id) in workSeq.workPoses \
                if seq is self.WORK else workSeq.waitPoses :
                item = QTableWidgetItem(str(pos))
                item.setData(Qt.UserRole, int(Id))
                table.setItem(row, (pos - 1), item)
                item.setTextAlignment(
                        Qt.AlignRight|Qt.AlignVCenter)
        table.resizeColumnsToContents()


if __name__ == '__main__' :
    import sys

    S = staffdata.StaffContainer()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
    S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12,13,14,15)
    S.staffsWork(S.NOR,1, 2, 3, 4, 6, 8, 9)
    #S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)

    app = QApplication(sys.argv)
    form = StaffListDialog(S)
    form.show()
    sys.exit(app.exec_())
