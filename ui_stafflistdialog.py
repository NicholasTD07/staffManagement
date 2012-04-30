# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_stafflistdialog.ui'
#
# Created: Wed Apr 25 23:40:19 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_StaffListDialog(object):
    def setupUi(self, StaffListDialog):
        StaffListDialog.setObjectName(_fromUtf8("StaffListDialog"))
        StaffListDialog.resize(600, 370)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(StaffListDialog.sizePolicy().hasHeightForWidth())
        StaffListDialog.setSizePolicy(sizePolicy)
        StaffListDialog.setMinimumSize(QtCore.QSize(600, 370))
        self.verticalLayout = QtGui.QVBoxLayout(StaffListDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(StaffListDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(StaffListDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.IdSpinBox = QtGui.QSpinBox(StaffListDialog)
        self.IdSpinBox.setMinimum(1)
        self.IdSpinBox.setMaximum(399)
        self.IdSpinBox.setObjectName(_fromUtf8("IdSpinBox"))
        self.horizontalLayout_2.addWidget(self.IdSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.TabWidget = QtGui.QTabWidget(StaffListDialog)
        self.TabWidget.setObjectName(_fromUtf8("TabWidget"))
        self.allStaffTab = QtGui.QWidget()
        self.allStaffTab.setObjectName(_fromUtf8("allStaffTab"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.allStaffTab)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.allTable = QtGui.QTableWidget(self.allStaffTab)
        self.allTable.setObjectName(_fromUtf8("allTable"))
        self.allTable.setColumnCount(0)
        self.allTable.setRowCount(0)
        self.horizontalLayout.addWidget(self.allTable)
        self.TabWidget.addTab(self.allStaffTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.TabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(StaffListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(StaffListDialog)
        self.TabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), StaffListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), StaffListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StaffListDialog)
        StaffListDialog.setTabOrder(self.IdSpinBox, self.allTable)
        StaffListDialog.setTabOrder(self.allTable, self.buttonBox)
        StaffListDialog.setTabOrder(self.buttonBox, self.TabWidget)

    def retranslateUi(self, StaffListDialog):
        StaffListDialog.setWindowTitle(QtGui.QApplication.translate("StaffListDialog", "查看员工队列", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("StaffListDialog", "查看工作队列:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setToolTip(QtGui.QApplication.translate("StaffListDialog", "在表中快速定位该名员工", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("StaffListDialog", "员工工号:", None, QtGui.QApplication.UnicodeUTF8))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.allStaffTab), QtGui.QApplication.translate("StaffListDialog", "所有员工", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    StaffListDialog = QtGui.QDialog()
    ui = Ui_StaffListDialog()
    ui.setupUi(StaffListDialog)
    StaffListDialog.show()
    sys.exit(app.exec_())

