# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_groupstaffdialog.ui'
#
# Created: Wed Apr 18 21:03:13 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_GroupStaffDialog(object):
    def setupUi(self, GroupStaffDialog):
        GroupStaffDialog.setObjectName(_fromUtf8("GroupStaffDialog"))
        GroupStaffDialog.resize(485, 330)
        self.gridLayout = QtGui.QGridLayout(GroupStaffDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        spacerItem = QtGui.QSpacerItem(145, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.addGroupButton = QtGui.QPushButton(GroupStaffDialog)
        self.addGroupButton.setObjectName(_fromUtf8("addGroupButton"))
        self.gridLayout.addWidget(self.addGroupButton, 0, 2, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(GroupStaffDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.unGrpTable = QtGui.QTableView(GroupStaffDialog)
        self.unGrpTable.setObjectName(_fromUtf8("unGrpTable"))
        self.verticalLayout.addWidget(self.unGrpTable)
        self.gridLayout.addLayout(self.verticalLayout, 1, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(GroupStaffDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.groupedTable = QtGui.QTableView(GroupStaffDialog)
        self.groupedTable.setObjectName(_fromUtf8("groupedTable"))
        self.verticalLayout_2.addWidget(self.groupedTable)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 1, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(GroupStaffDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 1, 1, 2)

        self.retranslateUi(GroupStaffDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), GroupStaffDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), GroupStaffDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(GroupStaffDialog)
        GroupStaffDialog.setTabOrder(self.addGroupButton, self.unGrpTable)
        GroupStaffDialog.setTabOrder(self.unGrpTable, self.groupedTable)
        GroupStaffDialog.setTabOrder(self.groupedTable, self.buttonBox)

    def retranslateUi(self, GroupStaffDialog):
        GroupStaffDialog.setWindowTitle(QtGui.QApplication.translate("GroupStaffDialog", "员工分组", None, QtGui.QApplication.UnicodeUTF8))
        GroupStaffDialog.setToolTip(QtGui.QApplication.translate("GroupStaffDialog", "1", None, QtGui.QApplication.UnicodeUTF8))
        self.addGroupButton.setText(QtGui.QApplication.translate("GroupStaffDialog", "添加分组", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("GroupStaffDialog", "未分组员工:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("GroupStaffDialog", "已分组员工:", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    GroupStaffDialog = QtGui.QDialog()
    ui = Ui_GroupStaffDialog()
    ui.setupUi(GroupStaffDialog)
    GroupStaffDialog.show()
    sys.exit(app.exec_())

