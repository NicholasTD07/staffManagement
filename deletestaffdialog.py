#!/usr/bin/python3
# File Info :
#   The DeleteStaffDialog class defined in this file.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import staffdata
import ui_deletestaffdialog


class DeleteStaffDialog(QDialog,
        ui_deletestaffdialog.Ui_DeleteStaffDialog) :
    
    def __init__(self, staffs, staff=None, parent=None) :
        super(DeleteStaffDialog, self).__init__(parent)
        self.setupUi(self)

        self.staffs = staffs
        self.staff = staff
        if self.staff is None :
            self.messageLabel.setText("请输入员工工号")
        else :
            self.Id = self.staff.Id
            self.updateLabels(self.staff)
        self.buttonBox.button(QDialogButtonBox.Ok).setText(
                                "确认删除")
        self.buttonBox.button(QDialogButtonBox.Cancel).setText(
                                "放弃")

    def accept(self) :
        print("删除员工: 点击了确认键")
        reply = QMessageBox.question(self,
                    "确认操作?",
                    "确认删除工号为: {} 的员工吗?".format(self.Id),
                    QMessageBox.Yes|QMessageBox.No)
        if reply == QMessageBox.Yes :
           print("删除员工: 点击了确定")
           self.staffs.deleteStaff(self.Id)
           QDialog.accept(self)
        
    @pyqtSignature("int")
    def on_IdSpinBox_valueChanged(self, Id) :
        staff = self.staffs.getStaff(Id)
        if staff is False :
            QMessageBox.warning(self,
            "员工工号错误",
            "没有此员工工号,请确认.")
            return
        self.Id = staff.Id
        self.updateLabels(staff)

    def updateLabels(self, staff) :
        self.IdSpinBox.setValue(staff.Id)
        self.nameLabel.setText("{}".format(staff.name))
        self.genderLabel.setText("{}".format(staff.gender))
        self.wTimeLabel.setText("{}".format(staff.wTime))
        wType = staff.wType
        self.wTypeLabel.setText("{}".format(wType))
        if wType is self.staffs.workTypes :
            self.workTypeLabel.setText("工作位置:")
            self.wPosLabel.setText("{}".format(staff.workPos))
        elif wType is self.staffs.WAIT :
            self.workTypeLabel.setText("等待位置:")
            self.wPosLabel.setText("{}".format(staff.waitPos))
        else :
            self.workTypeLabel.setText("")
            self.wPosLabel.setText("")
        self.messageLabel.setText("当前员工: {}".format(staff.Id))


if __name__ == '__main__' :
    import sys

    S = staffdata.StaffContainer()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9)

    app = QApplication(sys.argv)
    form = DeleteStaffDialog(S, S.getStaff(8))
    form.show()
    sys.exit(app.exec_())
