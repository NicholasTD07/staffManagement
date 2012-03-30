# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_stafflistdialog.ui'
#
# Created: Fri Mar 30 14:56:32 2012
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
        StaffListDialog.resize(565, 346)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(StaffListDialog.sizePolicy().hasHeightForWidth())
        StaffListDialog.setSizePolicy(sizePolicy)
        StaffListDialog.setMinimumSize(QtCore.QSize(565, 346))
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
        self.allStuffTab = QtGui.QWidget()
        self.allStuffTab.setObjectName(_fromUtf8("allStuffTab"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.allStuffTab)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.allTable = QtGui.QTableWidget(self.allStuffTab)
        self.allTable.setObjectName(_fromUtf8("allTable"))
        self.allTable.setColumnCount(0)
        self.allTable.setRowCount(0)
        self.horizontalLayout.addWidget(self.allTable)
        self.TabWidget.addTab(self.allStuffTab, _fromUtf8(""))
        self.workPosTab = QtGui.QWidget()
        self.workPosTab.setObjectName(_fromUtf8("workPosTab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.workPosTab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_3 = QtGui.QLabel(self.workPosTab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.workTable = QtGui.QTableWidget(self.workPosTab)
        self.workTable.setObjectName(_fromUtf8("workTable"))
        self.workTable.setColumnCount(0)
        self.workTable.setRowCount(0)
        self.verticalLayout_2.addWidget(self.workTable)
        self.TabWidget.addTab(self.workPosTab, _fromUtf8(""))
        self.waitPosTab = QtGui.QWidget()
        self.waitPosTab.setObjectName(_fromUtf8("waitPosTab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.waitPosTab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_4 = QtGui.QLabel(self.waitPosTab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_3.addWidget(self.label_4)
        self.waitTable = QtGui.QTableWidget(self.waitPosTab)
        self.waitTable.setObjectName(_fromUtf8("waitTable"))
        self.waitTable.setColumnCount(0)
        self.waitTable.setRowCount(0)
        self.verticalLayout_3.addWidget(self.waitTable)
        self.TabWidget.addTab(self.waitPosTab, _fromUtf8(""))
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
        StaffListDialog.setTabOrder(self.allTable, self.workTable)
        StaffListDialog.setTabOrder(self.workTable, self.waitTable)
        StaffListDialog.setTabOrder(self.waitTable, self.buttonBox)
        StaffListDialog.setTabOrder(self.buttonBox, self.TabWidget)

    def retranslateUi(self, StaffListDialog):
        StaffListDialog.setWindowTitle(QtGui.QApplication.translate("StaffListDialog", "查看员工队列", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("StaffListDialog", "查看工作队列:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setToolTip(QtGui.QApplication.translate("StaffListDialog", "在表中快速定位该名员工", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("StaffListDialog", "员工工号:", None, QtGui.QApplication.UnicodeUTF8))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.allStuffTab), QtGui.QApplication.translate("StaffListDialog", "所有员工", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("StaffListDialog", "提示:下表序号是员工所在队列中所排序号(不是员工工号).", None, QtGui.QApplication.UnicodeUTF8))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.workPosTab), QtGui.QApplication.translate("StaffListDialog", "工作序号", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("StaffListDialog", "提示:下表序号是员工所在队列中所排序号(不是员工工号).", None, QtGui.QApplication.UnicodeUTF8))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.waitPosTab), QtGui.QApplication.translate("StaffListDialog", "等待序号", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    StaffListDialog = QtGui.QDialog()
    ui = Ui_StaffListDialog()
    ui.setupUi(StaffListDialog)
    StaffListDialog.show()
    sys.exit(app.exec_())

