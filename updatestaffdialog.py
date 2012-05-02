#!/usr/bin/python3
# File Info : 
#   The UpdateStaffDialog class defined in this file.

# PyQt #
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# 引用#
import staffdata
import ui_updatestaffdialog

# 正则 #
import re


class UpdateStaffDialog(QDialog,
        ui_updatestaffdialog.Ui_UpdateStaffDialog) :

    def __init__(self, staffs, staff=None, parent=None) :
        super(UpdateStaffDialog, self).__init__(parent)
        self.setupUi(self)

        self.staffs = staffs
        self.workSeqs = staffs.getWorkSeq()
        self.staff = staff
        self.unavaliableIDs = []
        if staff is not None :
            # 1. 获得员工信息
            Id = staff.Id
            name = staff.name
            gender = staff.gender
            wTime = staff.wTime
            wType = staff.wType
            if wType == self.staffs.IDLE :
                pos = None
            else :
                nSeq = self.workSeqs[wTime].nSeq
                pos = nSeq.index(staff)
            # 2. 设置显示文字
            self.IdLineEdit.setText("{}".format(Id))
            self.IdLineEdit.setReadOnly(True)
            self.nameLineEdit.setText(name)
            self.genderComboBox.setCurrentIndex(
                self.genderComboBox.findText(gender))
            self.wTimeLabel.setText("{}".format(wTime))
            self.wTypeLabel.setText("{}".format(wType))
            if wType is self.staffs.WAIT :
                self.posNameLabel.setText("等待位置")
                self.posLabel.setText("{}".format(pos))
            elif staff.wType in staffs.workTypes :
                self.posNameLabel.setText("{}位置".format(wType))
                self.posLabel.setText("{}".format(pos))
            else :
                self.posNameLabel.setText("")
                self.posLabel.setText("")
                print("员工工作类型: {}".format(wType))
            self.buttonBox.button(QDialogButtonBox.Ok).setText(
                                    "确认修改(&A)")
            self.buttonBox.button(QDialogButtonBox.Cancel).setText(
                                    "放弃修改")
            self.setWindowTitle("编辑员工信息")
            self.nameLineEdit.setFocus()
        else :
            self.IdLineEdit.setFocus()
            self.posNameLabel.setText("")
            self.posLabel.setText("")
            self.wTimeLabel.setText("无")
            self.wTypeLabel.setText("无")

    # 重定义: 确定键 #

    def accept(self) :
        print("点击了确定键")
        updateStaff = self.staffs.updateStaff
        name = self.nameLineEdit.text()
        gender = self.getGender()
        if self.staff is None :
            print("添加模式")
            p = re.compile(r'\D+')
            rawdata = self.IdLineEdit.text()
            IDs = [ int(i) for i
                in re.split(p, rawdata) ]
            print("输入的员工序号: {}".format(IDs))
            if self.checkAndWarn(IDs=IDs) :
                print("已有员工工号,提示!")
                QMessageBox.warning(self,
                        "员工工号错误",
                        "请查询后重新输入"
                        "已有工号:\n"
                        "{}".format(self.unavaliableIDs))
                self.IdLineEdit.clear()
                self.unavaliableIDs = []
                return
            else :
                for Id in IDs :
                    print("没有该工号")
                    updateStaff(Id, gender, name)
                    print("新建成功!")
            QMessageBox.information(self,
                "操作成功!",
                "员工添加成功!\t\n"
                "工号: {}\n姓名: {}\n性别: {}"\
                    .format(self.IdLineEdit.text(),
                        self.nameLineEdit.text(),
                        self.genderComboBox.currentText()))
        else :
            Id = self.staff.Id
            name = self.nameLineEdit.text()
            QMessageBox.information(self,
                "操作成功!",
                "成功修改员工信息!\t\n"
                "工号: {}".format(Id))
            updateStaff(Id=Id,gender=gender,
                                name=name)
        QDialog.accept(self)

    #---- 辅助函数 ----#

    # 检查 Id 有效性 #

    def checkAndWarn(self, IDs=None) :
        if IDs is not None :
            for Id in IDs :
                print("检查序号: {}".format(Id))
                if self.staffs.getStaff(Id) :
                    self.unavaliableIDs.append(Id)
            return self.unavaliableIDs

    # 取得员工性别 #

    def getGender(self) :
        if self.genderComboBox.currentIndex() is 0 :
            return self.staffs.MALE
        elif self.genderComboBox.currentIndex() is 1 :
            return self.staffs.FEMALE

if __name__ == "__main__":
    import sys

    S = staffdata.StaffContainer()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9)
    S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    S.staffsWork(S.NOR, 4, 5, 6, 7, 8, 9)
    S.staffsWork(S.SEL, 1,2)
    S.staffsWork(S.NAMED, 3)

    app = QApplication(sys.argv)
    #form = UpdateStaffDialog(S, S.getStaff(3))
    form = UpdateStaffDialog(S)
    form.show()
    sys.exit(app.exec_())

