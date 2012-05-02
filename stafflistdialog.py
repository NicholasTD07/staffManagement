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
import updatestaffdialog


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
        # 载入: 员工, 员工序列
        self.staffs = staffs
        self.workSeqs = staffs.getWorkSeq()
        self.workTypes = staffs.workTypes

        # 生成: 所有员工表, 工作员工表, 等待员工表
        self.populateAll()
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
            return
        # 定位: 所有员工表
        self.allTable.setCurrentCell(0, Id - 1)

    # 双击: 所有员工表 #
    #@pyqtSignature("int,int")
    def on_allTable_cellDoubleClicked(self, row, column) :
        print("检测到双击所有员工表")
        item = self.allTable.item(0, column)
        self.updateStaff(item, column)

    #---- 辅助函数 ----#
    
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
            self.updateItem(column, Id)

    #---- 生成表格 ----#

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
        allTable = self.allTable
        setItem = allTable.setItem
        # 表头 #
        heads = [ str(i) for i in IDs ]
        vHeads = [ "员工工号", "姓名", "性别", "工作次数",
                "工作类型", "等待位置", "工作位置" ]
        # 清除: 已有内容
        allTable.clear()
        # 初始化: 设置 
        allTable.setSortingEnabled(False)
        allTable.setRowCount(len(vHeads))
        allTable.setColumnCount(len(heads))
        # 设置: 表头
        allTable.setVerticalHeaderLabels(vHeads)
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
        allTable.resizeColumnsToContents()


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
