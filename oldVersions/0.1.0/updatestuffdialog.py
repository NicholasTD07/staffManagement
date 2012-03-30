#!/usr/bin/python3
# File Info : 
#   The UpdateStuffDialog class defined in this file.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import stuffdata
import ui_updatestuffdialog

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
            if stuff.wType is stuffs.WAIT :
                self.waitPosSpinBox.setEnabled(True)
                self.waitPosSpinBox.setValue(stuff.waitPos)
            elif stuff.wType is (stuffs.NOR or
                                stuffs.SEL or stuffs.NAMED) :
                self.workPosSpinBox.setEnabled(True)
                self.workPosSpinBox.setValue(stuff.workPos)
            self.buttonBox.button(QDialogButtonBox.Ok).setText(
                                    "确认修改(&A)")
            self.setWindowTitle("编辑员工信息")
        else :
            self.nameLineEdit.setFocus()

    @pyqtSignature("QString")
    def on_wTypeComboBox_currentIndexChanged(self, text) :
        self.updateDialog(text)

    @pyqtSignature("int")
    def on_waitPosSpinBox_

    def updateDialog(self,text) :
        if text is (stuffs.NOR or
                            stuffs.SEL or stuffs.NAMED) :
            self.workPosSpinBox.setEnabled(True)
        elif text is stuffs.WAIT :
            self.waitPosSpinBox.setEnabled(True)
