#!/usr/bin/python3
# File Info :
#   The DeleteStuffDialog class defined in this file.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import stuffdata
import ui_deletestuffdialog


__version__="0.1.0"


class DeleteStuffDialog(QDialog,
        ui_deletestuffdialog.Ui_DeleteStuffDialog) :
    
    def __init__(self, stuffs, stuff=None, parent=None) :
        super(DeleteStuffDialog, self).__init__(parent)
        self.setupUi(self)

        self.stuffs = stuffs
        self.stuff = stuff
        if self.stuff is None :
            self.messageLabel.setText("请输入员工工号")
        else :
            self.Id = self.stuff.Id
            self.updateLabels(self.stuff)
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
        if reply is QMessageBox.Yes :
           self.stuffs.deleteStuff(self.Id)
           QDialog.accept(self)
        
    @pyqtSignature("int")
    def on_IdSpinBox_valueChanged(self, Id) :
        stuff = self.stuffs.stuffId(Id)
        if stuff is False :
            QMessageBox.warning(self,
            "员工工号错误",
            "没有此员工工号,请确认.")
            return
        self.Id = stuff.Id
        self.updateLabels(stuff)

    def updateLabels(self, stuff) :
        self.IdSpinBox.setValue(stuff.Id)
        self.nameLabel.setText("{}".format(stuff.name))
        self.genderLabel.setText("{}".format(stuff.gender))
        self.wTimeLabel.setText("{}".format(stuff.wTime))
        wType = stuff.wType
        self.wTypeLabel.setText("{}".format(wType))
        if wType is (self.stuffs.NOR or self.stuffs.SEL or
                                        self.stuffs.NAMED) :
            self.workTypeLabel.setText("工作位置:")
            self.wPosLabel.setText("{}".format(stuff.workPos))
        elif wType is self.stuffs.WAIT :
            self.workTypeLabel.setText("等待位置:")
            self.wPosLabel.setText("{}".format(stuff.waitPos))
        else :
            self.workTypeLabel.setText("")
            self.wPosLabel.setText("")
        self.messageLabel.setText("当前员工: {}".format(stuff.Id))


if __name__ == '__main__' :
    import sys

    S = stuffdata.StuffContainer()
    S.addStuffs(S.MALE, 1,2,3,4,5,6,7,8,9)

    app = QApplication(sys.argv)
    form = DeleteStuffDialog(S, S.stuffId(8))
    form.show()
    sys.exit(app.exec_())
