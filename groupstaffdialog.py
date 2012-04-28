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

class GroupStaffDialog(QDialog) :

    def __init__(self, staffs, parent=None) :
        # 初始化 #
        super(GroupStaffDialog, self).__init__(parent)

        # 获取员工分组信息 #
        self.staffs = staffs
        self.unGrpIDs = staffs.getUngrpStaff()
        self.groups = staffs.getGroups()

        # 内部变量 #
        self.lastColumn = {}

        # 设置界面 #
        self.setupUi()

        #---- 更新内容 ----#

        # 更新表格 #
        self.updateUnGrpTable()
        self.updateGroupedTable()


        #---- 自定义信号 ----#

        # 添加分组按键 #
        self.connect(self.addGroupButton, SIGNAL("clicked()"),
                lambda : self.groups.append([]))
                #lambda : print("点击按键"))

        # 添加至分组按键 #
        self.connect(self.whichGroupButton, SIGNAL("clicked()"),
                self.on_whichGroupButton_clicked)

        # 数字框 #
        self.connect(self.groupSpinBox, SIGNAL("valueChanged(int)"),
                self.on_groupSpinBox_valueChanged)
                #lambda : print("点击按键"))

        # 链接信号 #
        self.connect(self.buttonBox, SIGNAL("accepted()"),
                        self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"),
                        self.reject)

    #---- 设置界面 ----#
    def setupUi(self) :
        #-- 添加组件 --#
        # 标签 #
        self.unGrpLabel = QLabel("未分组员工序号:", self)
        self.groupedLabel = QLabel("已分组员工序号:", self)
        self.whichGroupLabel = QLabel("组号:",self)

        # 数字框 #
        groupSpinBox = QSpinBox(self)
        groupSpinBox.setRange(1, len(self.groups))
        groupSpinBox.setValue(1)
        self.groupSpinBox = groupSpinBox

        # 按键 #
        self.addGroupButton = QPushButton()
        self.addGroupButton.setText("添加分组")
        self.whichGroupButton = QPushButton()
        self.whichGroupButton.setText("添加至第1分组")

        # 按键组 #
        buttonBox = QDialogButtonBox(self)
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(
                QDialogButtonBox.Cancel
                | QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Cancel).setText("放弃修改")
        buttonBox.button(QDialogButtonBox.Ok).setText("确认修改")
        self.buttonBox = buttonBox

        # 表格 #
        self.unGrpTable = QTableWidget(self)
        self.groupedTable = QTableWidget(self)

        #---- 组织结构 ----#

        # 上(横向) #
        HBoxLayout  = QHBoxLayout()
        HBoxLayout.addItem(QSpacerItem(145, 20,
                QSizePolicy.Expanding, QSizePolicy.Minimum))
        HBoxLayout.addWidget(self.addGroupButton)

        # 下左(纵向) #
        VBoxLayoutL = QVBoxLayout()
        VBoxLayoutL.addWidget(self.unGrpLabel)
        VBoxLayoutL.addWidget(self.unGrpTable)

        # 下中(纵向) #
        VBoxLayoutM = QVBoxLayout()
        VBoxLayoutM.addStretch()
        VBoxLayoutM.addWidget(self.whichGroupLabel)
        VBoxLayoutM.addWidget(self.groupSpinBox)
        VBoxLayoutM.addWidget(self.whichGroupButton)
        VBoxLayoutM.addStretch()

        # 下右(纵向) #
        VBoxLayoutR = QVBoxLayout()
        VBoxLayoutR.addWidget(self.groupedLabel)
        VBoxLayoutR.addWidget(self.groupedTable)

        # 挂入对话框 #
        self.HBoxLayout = HBoxLayout
        self.VBoxLayoutL = VBoxLayoutL
        self.VBoxLayoutM = VBoxLayoutM
        self.VBoxLayoutR = VBoxLayoutR

        # 对话框结构 #
        gridLayout = QGridLayout()
        addLayout = gridLayout.addLayout
        addLayout(self.HBoxLayout, 0, 2, 1, 1)
        addLayout(self.VBoxLayoutL, 1, 0, 1, 1)
        addLayout(self.VBoxLayoutM, 1, 1, 1, 1)
        addLayout(self.VBoxLayoutR, 1, 2, 1, 1)
        gridLayout.addWidget(self.buttonBox, 2, 2, 1, 1)
        self.gridLayout = gridLayout

        # 设置属性 #
        self.setLayout(self.gridLayout)
        self.resize(540, 330)
        self.setWindowTitle("员工分组")

    #---- 重定义函数 ----#

    def accept(self) :
        reply = QMessageBox.question(self,
                    "员工分组: 尚未保存",
                    "是否保存员工分组?",
                    QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.Yes :
            self.saveGroups()
        QDialog.accept(self)

    #---- 辅助函数 ----#
    def saveGroups(self) :
        # 初始化局部变量 #
        unGrpIDs = self.unGrpIDs
        groups = self.groups
        groupedTable = self.groupedTable
        row = 0
        rows = {}
        rowCount = groupedTable.rowCount()
        # 获取每行的员工工号 #
        while row < rowCount :
            # 初始化循环变量 #
            group = groups[row]
            rows[row] = []
            thisRow = rows[row]
            groupedTable.selectRow(row)
            items = groupedTable.selectedItems()
            for item in items :
                Id = int(item.data(Qt.UserRole))
                thisRow.append(Id)
                unGrpIDs.remove(Id)
            group = group + \
                    [ Id for Id in thisRow if Id not in group ]
            print("row:", row, "\n", "group:", group)
            row += 1

    #---- 自定义槽 ----#

    #-- 数字框信号槽 --# 
    def on_groupSpinBox_valueChanged(self) :
        # 初始化局部变量 #
        groups = self.groups
        spinBox = self.groupSpinBox
        value = spinBox.value()
        maxGroups = len(groups)
        # 判断数据合法性 #
        if value <= maxGroups :
            self.whichGroupButton.setText("添加至第{}分组".format(value))
        else :
            QMessageBox.warning(self,
                    "设置分组",
                    "超出当前最大分组数.自动设置为当前最大值")
            spinBox.setValue(maxGroups)

    #-- 添加至分组按键信号槽 --#
    def on_whichGroupButton_clicked(self) :
        # 初始化局部变量 #
        unGrpTable = self.unGrpTable
        unGrpTablesetCurrentCell = unGrpTable.setCurrentCell
        groupedTable = self.groupedTable
        lastColumn = self.lastColumn
        row = self.groupSpinBox.value() - 1
        # 获取多选员工 #
        items = unGrpTable.selectedItems()
        # 检查合法性 #
        if items is None :
            QMessageBox.warning(self,
                    "请选择员工",
                    "尚未选择任何员工进行操作."
                    "\n请在未分组员工框内选择之后再进行操作.")
        for item in items :
            itemRow = unGrpTable.row(item)
            itemColumn = unGrpTable.column(item)
            Id = int(item.data(Qt.UserRole))
            # 弹出员工 #
            unGrpTable.takeItem(itemRow, itemColumn)
            # 取得列位置 #
            column = lastColumn[row]
            # 判断合法性 #
            if column + 1 >= groupedTable.columnCount() :
                groupedTable.insertColumn(column)
            # 插入员工 #
            groupedTable.setItem(row, column, item)
            groupedTable.setCurrentItem(item)
            # 更新内部变量 #
            lastColumn[row] += 1
        # 必须更新列大小 #
        groupedTable.resizeColumnsToContents()
        # 将选择员工放在下一个位置 #
        if itemColumn != 0 and itemColumn % 9 == 0 :
            unGrpTablesetCurrentCell(itemRow+1, 0)
        else :
            unGrpTablesetCurrentCell(itemRow, itemColumn+1)

    #---- 更新表格 ----#

    #-- 生成未分组员工表格 --#
    def updateUnGrpTable(self) :
        # 初始化局部变量 #
        i = 0
        unGrpIDs = self.unGrpIDs
        unGrpTable = self.unGrpTable
        lenIDs = len(unGrpIDs)
        # 清除已有内容
        unGrpTable.clear()
        # 初始化设置 
        unGrpTable.setSortingEnabled(False)
        unGrpTable.setRowCount(int(lenIDs/10)+1)
        unGrpTable.setColumnCount(10)
        # 更新表格内容 #
        while i < lenIDs:
            Id = unGrpIDs[i]
            item = QTableWidgetItem(str(Id))
            item.setData(Qt.UserRole, int(Id))
            item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
            unGrpTable.setItem(i // 10, i % 10, item)
            i += 1
        unGrpTable.resizeColumnsToContents()

    #-- 生成分组员工表格 --#
    def updateGroupedTable(self) :
        # 初始化局部变量 #
        groups = self.groups
        groupedTable = self.groupedTable
        lastColumn = self.lastColumn
        lenGroups = len(groups)
        row = 0
        maxColumn = 0
        for group in groups :
            column = len(group)
            if column > maxColumn :
                maxColumn = column
        maxColumn += 10
        # 清除已有内容 #
        groupedTable.clear()
        # 初始化设置 #
        groupedTable.setSortingEnabled(False)
        groupedTable.setRowCount(lenGroups)
        groupedTable.setColumnCount(maxColumn)
        # 更新表格内容 #
        for group in groups :
            column = 0
            lastColumn[row] = 0
            for Id in group :
                item = QTableWidgetItem(str(Id))
                item.setData(Qt.UserRole, int(Id))
                item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
                unGrpTable.setItem(row, column, item)
                column += 1
            lastColumn[row] = column
            row += 1
        groupedTable.resizeColumnsToContents()


if __name__ == "__main__" :
    import sys
    app = QApplication(sys.argv)

    S = staffdata.StaffContainer()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)

    form = GroupStaffDialog(S)
    form.show()
    sys.exit(app.exec_())
