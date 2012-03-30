#!/usr/bin/python3
# File Info : 
#   The UpdateStuffDialog class defined in this file.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import stuffdata
import ui_updatestuffdialog

__version__="0.1.0"

class UpdateStuffDialog(QDialog,
        ui_updatestuffdialog.Ui_UpdateStuffDialog) :

    def __init__(self, stuffs, stuff=None, parent=None) :
        super(UpdateStuffDialog, self).__init__(parent)
        self.setupUi(self)

        self.stuffs = stuffs
        self.stuff = stuff
        if stuff is not None :
            self.IdSpinBox.setValue(stuff.Id)
            self.IdSpinBox.isReadOnly()
            self.nameLineEdit.setText(stuff.name)
            self.genderComboBox.setCurrentIndex(
                self.genderComboBox.findText(stuff.gender))
            self.wTimeSpinBox.setEnabled(True)
            self.wTimeSpinBox.setValue(stuff.wTime)
            self.wTypeComboBox.setEnabled(True)
            self.wTypeComboBox.setCurrentIndex(
                self.wTypeComboBox.findText(stuff.wType))
            if stuff.wType is self.stuffs.WAIT :
                self.waitPosSpinBox.setEnabled(True)
                self.waitPosSpinBox.setValue(stuff.waitPos)
            elif stuff.wType is (self.stuffs.NOR or
                    self.stuffs.SEL or self.stuffs.NAMED) :
                self.workPosSpinBox.setEnabled(True)
                self.workPosSpinBox.setValue(stuff.workPos)
            self.buttonBox.button(QDialogButtonBox.Ok).setText(
                                    "确认修改(&A)")
            self.setWindowTitle("编辑员工信息")
        else :
            self.nameLineEdit.setFocus()

    @pyqtSignature("int")
    def on_wTypeComboBox_currentIndexChanged(self, index) :
        self.updateDialog(index)

    def updateDialog(self, index) :
        if index is (0 or 1 or 2) :
            self.workPosSpinBox.setEnabled(True)
        elif index is 3 :
            self.waitPosSpinBox.setEnabled(True)

    def checkAndWarn(self, Id=None, wTime=0,
            waitPos=None, workPos=None) :
        if Id is not None :
            if self.stuffs.stuffId(Id) :
                QMessageBox.warning(self, "员工工号错误",
                        "已有此工号."
                        "请查询后重新输入")
                #self.IdSpinBox.setValue(0)
                return False
        if waitPos is not None :
            if not self.stuffs.waitPosAvaliable(wTime,
                                    waitPos) :
                QMessageBox.warning(self, "员工等待位置错误",
                        "此等待位置已有员工."
                        "请查询后重新输入")
                return False
        if workPos is not None :
            if not self.stuffs.workPosAvaliable(wTime,
                                    waitPos) :
                QMessageBox.warning(self, "员工工作位置错误",
                        "此工作位置已有员工."
                        "请查询后重新输入")
                return False
        return True

    def getWorkType(self) :
        if self.wTypeComboBox.currentIndex() is 0 :
            return self.stuffs.NOR
        elif self.wTypeComboBox.currentIndex() is 1 :
            return self.stuffs.NAMED
        elif self.wTypeComboBox.currentIndex() is 2 :
            return self.stuffs.SEL
        elif self.wTypeComboBox.currentIndex() is 3 :
            return self.stuffs.WAIT
        elif self.wTypeComboBox.currentIndex() is 4 :
            return self.stuffs.IDLE

    def getGender(self) :
        if self.genderComboBox.currentIndex() is 0 :
            return self.stuffs.MALE
        elif self.genderComboBox.currentIndex() is 1 :
            return self.stuffs.FEMALE

    def accept(self) :
        print("点击了确定键")
        name = self.nameLineEdit.text()
        gender = self.getGender()
        if self.stuff is None :
            print("添加模式")
            Id = self.IdSpinBox.value()
            if not self.checkAndWarn(Id=Id) :
                print("已有员工工号,提示!")
                return
                #self.stuffs.updateStuff(Id=Id, gender=gender,
                #                name=name)
                print("没有该工号")
                self.stuffs.updateStuff(Id)
                print("新建成功!")
        else :
            wTime = self.wTimeSpinBox.value()
            wType = self.getWorkType()
            if wType is (self.stuffs.NOR or
                    self.stuffs.NAMED or self.stuffs.SEL) :
                workPos = self.workPosSpinBox.value()
                if not self.checkAndWarn(wTime=wTime,
                            workPos=workPos) :
                    return
                self.stuffs.setWorkPos(Id, workPos)
            elif wType is self.stuffs.WAIT :
                waitPos = self.waitPosSpinBox.value()
                if not self.checkAndWarn(wTime=wTime,
                            waitPos=workPos) :
                    return
                self.stuffs.setWaitPos(Id, waitPos)
        self.stuffs.updateStuff(Id=Id,gender=gender,
                            name=name)
        self.stuffs.tell(Id)
        QDialog.accept(self)


if __name__ == "__main__":
    import sys

    S = stuffdata.StuffContainer()
    S.addStuffs(S.MALE, 1,2,3,4,5,6,7,8,9)

    app = QApplication(sys.argv)
    form = UpdateStuffDialog(S)
    form.show()
    sys.exit(app.exec_())

