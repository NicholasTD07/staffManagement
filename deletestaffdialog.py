#!/usr/bin/python3
# File Info :
#   The DeleteStaffDialog class defined in this file.

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

# 引用#
import staffdata


class DeleteStaffDialog(QDialog) :

    
    #{{{ # 初始化更新员工信息窗口 #
    def __init__(self, staffs, staff=None, parent=None) :
        super(DeleteStaffDialog, self).__init__(parent)
        self.staff = staff
        self.staffs = staffs
        self.setupUi()

        if self.staff is None :
            self.currentIdLabel.setText("请输入员工工号")
        else :
            self.Id = self.staff.Id
            self.updateLabels(self.staff)

        # 链接信号 #
        self.connect(self.IdSpinBox, SIGNAL("valueChanged(int)"),
                self.on_IdSpinBox_valueChanged)
        self.connect(self.buttonBox, SIGNAL("accepted()"),
                        self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"),
                        self.reject)
    #}}}

    #{{{ # 设置界面 #
    def setupUi(self) :
        #-- 添加组件 --#

        # 标签 #
        self.currentIdLabel = QLabel("", self)
        self.nameLabel = QLabel("", self)
        self.nameLabel.setAlignment(Qt.AlignRight)
        self.genderLabel = QLabel("", self)
        self.genderLabel.setAlignment(Qt.AlignRight)
        self.groupLabel = QLabel("", self)
        self.groupLabel.setAlignment(Qt.AlignRight)
        self.workTimeLabel = QLabel("", self)
        self.workTimeLabel.setAlignment(Qt.AlignRight)
        self.workTypeLabel = QLabel("", self)
        self.workTypeLabel.setAlignment(Qt.AlignRight)
        self.typePosLabel = QLabel("", self)
        self.posLabel = QLabel("", self)
        self.posLabel.setAlignment(Qt.AlignRight)

        # 数字框 #
        self.IdSpinBox = QSpinBox(self)
        self.IdSpinBox.setRange(0, len(self.staffs))

        # 分割线 #
        Hline = QFrame(self)
        Hline.setFrameShape(QFrame.HLine)
        Hline.setFrameShadow(QFrame.Sunken)

        # 按键组 #
        buttonBox = QDialogButtonBox(self)
        buttonBox.setOrientation(Qt.Horizontal)
        buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).setText("确认删除")
        buttonBox.button(QDialogButtonBox.Cancel).setText("放弃删除")
        # 挂入对话框 #
        self.buttonBox = buttonBox

        # 对话框结构 #
        gridLayout = QGridLayout()
        GaddWidget = gridLayout.addWidget
        GaddWidget(QLabel("员工工号:", self), 0, 0, 1, 1)
        GaddWidget(self.IdSpinBox, 0, 1, 1, 1)
        GaddWidget(QLabel("员工基本信息", self), 1, 0, 1, 1)
        GaddWidget(self.currentIdLabel, 1, 1, 1, 1)
        GaddWidget(QLabel("姓名:", self), 2, 0, 1, 1)
        GaddWidget(self.nameLabel, 2, 1, 1, 1)
        GaddWidget(QLabel("性别:", self), 3, 0, 1, 1)
        GaddWidget(self.genderLabel, 3, 1, 1, 1)
        GaddWidget(QLabel("分组:", self), 4, 0, 1, 1)
        GaddWidget(self.groupLabel, 4, 1, 1, 1)
        GaddWidget(Hline, 5, 0, 1, 2)
        GaddWidget(QLabel("员工工作状态", self), 6, 0 ,1 ,1)
        GaddWidget(QLabel("工作次数:", self), 7, 0, 1, 1)
        GaddWidget(self.workTimeLabel, 7, 1, 1, 1)
        GaddWidget(QLabel("工作类型:", self), 8, 0, 1, 1)
        GaddWidget(self.workTypeLabel, 8, 1, 1, 1)
        GaddWidget(self.typePosLabel, 9, 0, 1, 1)
        GaddWidget(self.posLabel, 9, 1, 1, 1)
        GaddWidget(QLabel("", self), 10, 0)
        GaddWidget(buttonBox, 11, 0, 1, 1)

        # 对话框属性 # 
        self.setLayout(gridLayout)
        self.resize(287, 338)
        self.setMinimumSize(QSize(287, 338))
        #}}}

    #{{{ # 重定义: 确定键 #
    def accept(self) :
        reply = QMessageBox.question(self,
                    "确认操作?",
                    "确认删除工号为: {} 的员工吗?".format(self.Id),
                    QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.Yes :
           self.staffs.deleteStaff(self.Id)
           QDialog.accept(self)
        
    def on_IdSpinBox_valueChanged(self, Id) :
        staff = self.staffs.getStaff(Id)
        if staff is False :
            QMessageBox.warning(self,
            "员工工号错误",
            "没有此员工工号,请确认.")
            return
        self.Id = staff.Id
        self.updateLabels(staff)
    #}}}

    #{{{ #---- 辅助函数 ----#
    def updateLabels(self, staff) :
        self.IdSpinBox.setValue(staff.Id)
        self.nameLabel.setText("{}".format(staff.name))
        self.genderLabel.setText("{}".format(staff.gender))
        self.groupLabel.setText("{}".format(
            staff. group if staff.group is not None else ""))
        self.workTimeLabel.setText("{}".format(staff.wTime))
        wType = staff.wType
        self.workTypeLabel.setText("{}".format(wType))
        if wType is self.staffs.IDLE :
            self.typePosLabel.setText("")
            pos = ""
        else :
            nSeq = self.staffs.getWorkSeq()[staff.wTime].nSeq
            pos = nSeq.index(staff)
            self.typePosLabel.setText("{}位置:".format(wType))
        self.posLabel.setText("{}".format(pos))
        self.currentIdLabel.setText("当前员工: {}".format(staff.Id))
    #}}}


if __name__ == '__main__' :
    import sys

    S = staffdata.StaffContainer()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9)
    S.updateStaff(8, name="TD")
    S.groupStaff(8, 1)
    #S.staffWork(8, S.NAMED)

    app = QApplication(sys.argv)
    form = DeleteStaffDialog(S, S.getStaff(8))
    form.show()
    sys.exit(app.exec_())
