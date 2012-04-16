# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_updatestaffdialog.ui'
#
# Created: Mon Apr 16 09:19:13 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_UpdateStaffDialog(object):
    def setupUi(self, UpdateStaffDialog):
        UpdateStaffDialog.setObjectName(_fromUtf8("UpdateStaffDialog"))
        UpdateStaffDialog.resize(426, 278)
        UpdateStaffDialog.setMinimumSize(QtCore.QSize(426, 278))
        self.horizontalLayout = QtGui.QHBoxLayout(UpdateStaffDialog)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(UpdateStaffDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.label = QtGui.QLabel(UpdateStaffDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(UpdateStaffDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.nameLineEdit = QtGui.QLineEdit(UpdateStaffDialog)
        self.nameLineEdit.setObjectName(_fromUtf8("nameLineEdit"))
        self.gridLayout.addWidget(self.nameLineEdit, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(UpdateStaffDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.genderComboBox = QtGui.QComboBox(UpdateStaffDialog)
        self.genderComboBox.setObjectName(_fromUtf8("genderComboBox"))
        self.genderComboBox.addItem(_fromUtf8(""))
        self.genderComboBox.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.genderComboBox, 3, 1, 1, 1)
        self.IdLineEdit = QtGui.QLineEdit(UpdateStaffDialog)
        self.IdLineEdit.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.IdLineEdit.setObjectName(_fromUtf8("IdLineEdit"))
        self.gridLayout.addWidget(self.IdLineEdit, 1, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 5)
        self.verticalLayout.addLayout(self.gridLayout)
        self.line = QtGui.QFrame(UpdateStaffDialog)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_5 = QtGui.QLabel(UpdateStaffDialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 0, 0, 1, 1)
        self.label_7 = QtGui.QLabel(UpdateStaffDialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)
        self.wTimeLabel = QtGui.QLabel(UpdateStaffDialog)
        self.wTimeLabel.setObjectName(_fromUtf8("wTimeLabel"))
        self.gridLayout_2.addWidget(self.wTimeLabel, 1, 1, 1, 1)
        self.label_6 = QtGui.QLabel(UpdateStaffDialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.wTypeLabel = QtGui.QLabel(UpdateStaffDialog)
        self.wTypeLabel.setObjectName(_fromUtf8("wTypeLabel"))
        self.gridLayout_2.addWidget(self.wTypeLabel, 2, 1, 1, 1)
        self.posNameLabel = QtGui.QLabel(UpdateStaffDialog)
        self.posNameLabel.setObjectName(_fromUtf8("posNameLabel"))
        self.gridLayout_2.addWidget(self.posNameLabel, 3, 0, 1, 1)
        self.posLabel = QtGui.QLabel(UpdateStaffDialog)
        self.posLabel.setObjectName(_fromUtf8("posLabel"))
        self.gridLayout_2.addWidget(self.posLabel, 3, 1, 1, 1)
        self.gridLayout_2.setColumnStretch(0, 5)
        self.gridLayout_2.setColumnStretch(1, 4)
        self.verticalLayout.addLayout(self.gridLayout_2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.line_2 = QtGui.QFrame(UpdateStaffDialog)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.horizontalLayout.addWidget(self.line_2)
        self.buttonBox = QtGui.QDialogButtonBox(UpdateStaffDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout.addWidget(self.buttonBox)

        self.retranslateUi(UpdateStaffDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), UpdateStaffDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), UpdateStaffDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(UpdateStaffDialog)

    def retranslateUi(self, UpdateStaffDialog):
        UpdateStaffDialog.setWindowTitle(QtGui.QApplication.translate("UpdateStaffDialog", "修改员工信息", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("UpdateStaffDialog", "员工基本信息:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("UpdateStaffDialog", "员工工号:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("UpdateStaffDialog", "姓名:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("UpdateStaffDialog", "性别:", None, QtGui.QApplication.UnicodeUTF8))
        self.genderComboBox.setItemText(0, QtGui.QApplication.translate("UpdateStaffDialog", "男", None, QtGui.QApplication.UnicodeUTF8))
        self.genderComboBox.setItemText(1, QtGui.QApplication.translate("UpdateStaffDialog", "女", None, QtGui.QApplication.UnicodeUTF8))
        self.IdLineEdit.setToolTip(QtGui.QApplication.translate("UpdateStaffDialog", "可用空格分隔多个员工工号, 方便批量创建员工.", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("UpdateStaffDialog", "员工工作状态:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setText(QtGui.QApplication.translate("UpdateStaffDialog", "工作次数:", None, QtGui.QApplication.UnicodeUTF8))
        self.wTimeLabel.setText(QtGui.QApplication.translate("UpdateStaffDialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("UpdateStaffDialog", "工作状态:", None, QtGui.QApplication.UnicodeUTF8))
        self.wTypeLabel.setText(QtGui.QApplication.translate("UpdateStaffDialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))
        self.posNameLabel.setText(QtGui.QApplication.translate("UpdateStaffDialog", "XX位置:", None, QtGui.QApplication.UnicodeUTF8))
        self.posLabel.setText(QtGui.QApplication.translate("UpdateStaffDialog", "TextLabel", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    UpdateStaffDialog = QtGui.QDialog()
    ui = Ui_UpdateStaffDialog()
    ui.setupUi(UpdateStaffDialog)
    UpdateStaffDialog.show()
    sys.exit(app.exec_())

