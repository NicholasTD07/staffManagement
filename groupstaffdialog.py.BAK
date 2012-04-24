#!/usr/bin/python3
# File Info :
#   员工分组对话框


# 系统 #
import sys

# PyQt #
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# 调用 #
import staffdata

# UI #
#import ui_groupdtaffdialog


class enDrgTable(QTableWidget) :

    def __init__(self, parent=None) :
        super(enDrgTable, self).__init__(parent)
        self.lastRow = 0
        self.lastColumn = 0
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)

    def dragEnterEvent(self, event) :
        if event.mimeData().hasText() :
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event) :
        if event.mimeData().hasText() :
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def startDrag(self, dropActions):
        item = self.currentItem()
        if item is None :
            return
        mimeData = QMimeData()
        mimeData.setText(str(item.data(Qt.UserRole)))
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        if drag.start(Qt.MoveAction) == Qt.MoveAction:
            self.takeItem(self.row(item), self.column(item))


class unGrpTable(enDrgTable) :

    def __init__(self, parent=None) :
        super(unGrpTable, self).__init__(parent)
        self.unUsedBox = []

    def startDrag(self, dropActions) :
        item = self.currentItem()
        if item is None :
            return
        self.thisRow = self.currentRow()
        self.thisColumn = self.currentColumn()
        pos = (self.thisRow, self.thisColumn)
        if pos not in self.unUsedBox :
            self.unUsedBox.append(pos)
        print("添加位置:", pos)
        print(self.unUsedBox)
        enDrgTable.startDrag(self, dropActions)


    def dropEvent(self, event):
        #if event.source() == self :
        #    self.unUsedBox.remove(pos)
        #    print("去除位置:", pos)
        #    print(self.unUsedBox)
        #    return
        # 初始化 #
        method_item = self.item # Method
        unUsedBox = self.unUsedBox
        thisRow = self.thisRow
        thisColumn = self.thisColumn
        # 移除有 item 的格子#
        for pos in unUsedBox :
            if pos[0] != self.thisRow and pos[1] != self.thisColumn :
                if method_item(pos[0], pos[1]) : # 去除有 item 的位置.
                    unUsedBox.remove(pos)
                    print("去除pos:", pos, "item(pos的结果)", method_item(pos[0], pos[1]))
        # 取得信息 #
        mimeData = event.mimeData()
        if mimeData.hasText() :
            text = mimeData.text()
            Id = int(text)
            item = QTableWidgetItem(text)
            item.setData(Qt.UserRole, int(Id))
        else :
            return
        if unUsedBox :
            print("unUsedBox 非空")
            for (row, column) in unUsedBox :
                if row != thisRow or column != thisColumn :
                    print("找到非自身位置! ", "(", row, column, ")")
                    print("unUsedBox : ", unUsedBox)
                    self.setItem(row, column, item)
                    unUsedBox.remove((row, column))
                    ItemSet = True
                    break
                else :
                    ItemSet = False
                    print(row, column)
                    print(thisRow, thisColumn)
        if not ItemSet :
            self.setItem(self.lastRow, self.lastColumn, item)
            print("现在的行:",self.lastRow,"现在的列:",self.lastColumn)
            if self.lastColumn < 9 :
                self.lastColumn += 1
            else :
                self.lastRow += 1
                self.lastColumn = 0
                self.insertRow(self.lastRow)
                print("下一行, 新增一行.")
            event.setDropAction(Qt.MoveAction)
            event.accept()
        else:
            event.ignore()


class GroupStaffDialog(QDialog) :

    def __init__(self, staffs, parent=None) :
        # 初始化 #
        super(GroupStaffDialog, self).__init__(parent)
        # 获取员工分组信息 #
        self.staffs = staffs
        self.unGrpIDs = staffs.getUngrpStaff()
        self.groups = staffs.getGroups()
        # 初始化局部变量 #
        self.lastRow = 0
        self.lastColumn = 0
        # 添加组件 #
        self.horSpacer = QSpacerItem(145, 20,
                QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.addGroupButton = QPushButton()
        self.addGroupButton.setText("添加分组")
        self.unGrpLabel = QLabel("未分组员工序号:", self)
        self.groupedLabel = QLabel("已分组员工序号:", self)
        self.unGrpTable = unGrpTable(self)
        self.groupedTable = enDrgTable(self)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(
                QDialogButtonBox.Cancel
                | QDialogButtonBox.Ok)
        self.buttonBox.button(QDialogButtonBox.Cancel).setText("退出")
        # 组织结构 #
        HBoxLayout  = QHBoxLayout()
        HBoxLayout.addItem(self.horSpacer)
        HBoxLayout.addWidget(self.addGroupButton)
        VBoxLayoutL = QVBoxLayout()
        VBoxLayoutL.addWidget(self.unGrpLabel)
        VBoxLayoutL.addWidget(self.unGrpTable)
        VBoxLayoutR = QVBoxLayout()
        VBoxLayoutR.addWidget(self.groupedLabel)
        VBoxLayoutR.addWidget(self.groupedTable)
        # 挂入对话框 #
        self.HBoxLayout = HBoxLayout
        self.VBoxLayoutL = VBoxLayoutL
        self.VBoxLayoutR = VBoxLayoutR
        # 对话框结构 #
        gridLayout = QGridLayout()
        addLyt = gridLayout.addLayout
        addLyt(self.HBoxLayout, 0, 1, 1, 1)
        addLyt(self.VBoxLayoutL, 1, 0, 1, 1)
        addLyt(self.VBoxLayoutR, 1, 1, 1, 1)
        gridLayout.addWidget(self.buttonBox, 2, 1, 1, 1)
        self.gridLayout = gridLayout
        # 设置属性 #
        self.setLayout(self.gridLayout)
        self.resize(460, 330)
        self.setWindowTitle("员工分组")
        # 链接信号 #
        self.connect(self.buttonBox, SIGNAL("accepted()"),
                        self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"),
                        self.reject)
        # 按键信号 #
        self.connect(self.addGroupButton, SIGNAL("clicked()"),
                        lambda : self.groups.append([]))
        # 更新表格 #
        self.updateUnGrpT()

    # 重定义: 按键事件 #

    def keyPressEvent(self, event) :
        if event.key() == Qt.Key_Enter :
            event.ignore()
        elif event.key() == Qt.Key_Escape :
            QDialog.reject(self)
        else :
            QWidget.keyPressEvent(self, event)

    # 更新表格 #
    def updateUnGrpT(self) :
        # 初始局部变量 #
        i = 0
        lastRow = 0
        lastColumn = 0
        unGrpIDs = self.unGrpIDs
        unGrpTable = self.unGrpTable
        length = len(unGrpIDs)
        # 清除: 已有内容
        unGrpTable.clear()
        # 初始化: 设置 
        unGrpTable.setSortingEnabled(False)
        unGrpTable.setRowCount(int(length/10)+1)
        unGrpTable.setColumnCount(10)
        while i < length :
            if i != 0 and i % 10 == 0 :
                lastRow += 1
                lastColumn = 0
                print("下一行.")
            print("局部变量 i: {}".format(i))
            Id = unGrpIDs[i]
            item = QTableWidgetItem(str(Id))
            item.setData(Qt.UserRole, int(Id))
            item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            unGrpTable.setItem(lastRow, lastColumn, item)
            lastColumn += 1
            i += 1
            print("员工序号:",Id)
        unGrpTable.resizeColumnsToContents()
        unGrpTable.lastRow = lastRow
        unGrpTable.lastColumn = lastColumn


if __name__ == "__main__" :
    import sys
    app = QApplication(sys.argv)

    S = staffdata.StaffContainer()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)

    form = GroupStaffDialog(S)
    form.show()
    sys.exit(app.exec_())
