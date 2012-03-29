# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_stufflistdialog_TabWidget.ui'
#
# Created: Sun Mar 11 22:18:28 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_StuffListDialog(object):
    def setupUi(self, StuffListDialog):
        StuffListDialog.setObjectName(_fromUtf8("StuffListDialog"))
        StuffListDialog.resize(565, 346)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(StuffListDialog.sizePolicy().hasHeightForWidth())
        StuffListDialog.setSizePolicy(sizePolicy)
        StuffListDialog.setMinimumSize(QtCore.QSize(565, 346))
        self.verticalLayout = QtGui.QVBoxLayout(StuffListDialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(StuffListDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label_2 = QtGui.QLabel(StuffListDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.IdSpinBox = QtGui.QSpinBox(StuffListDialog)
        self.IdSpinBox.setMaximum(399)
        self.IdSpinBox.setObjectName(_fromUtf8("IdSpinBox"))
        self.horizontalLayout_2.addWidget(self.IdSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.TabWidget = QtGui.QTabWidget(StuffListDialog)
        self.TabWidget.setObjectName(_fromUtf8("TabWidget"))
        self.allStuffTab = QtGui.QWidget()
        self.allStuffTab.setObjectName(_fromUtf8("allStuffTab"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.allStuffTab)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.allStuffTable = QtGui.QTableWidget(self.allStuffTab)
        self.allStuffTable.setObjectName(_fromUtf8("allStuffTable"))
        self.allStuffTable.setColumnCount(0)
        self.allStuffTable.setRowCount(0)
        self.horizontalLayout.addWidget(self.allStuffTable)
        self.TabWidget.addTab(self.allStuffTab, _fromUtf8(""))
        self.workPosTab = QtGui.QWidget()
        self.workPosTab.setObjectName(_fromUtf8("workPosTab"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.workPosTab)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_3 = QtGui.QLabel(self.workPosTab)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.workPosTable = QtGui.QTableWidget(self.workPosTab)
        self.workPosTable.setObjectName(_fromUtf8("workPosTable"))
        self.workPosTable.setColumnCount(0)
        self.workPosTable.setRowCount(0)
        self.verticalLayout_2.addWidget(self.workPosTable)
        self.TabWidget.addTab(self.workPosTab, _fromUtf8(""))
        self.waitPosTab = QtGui.QWidget()
        self.waitPosTab.setObjectName(_fromUtf8("waitPosTab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.waitPosTab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_4 = QtGui.QLabel(self.waitPosTab)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_3.addWidget(self.label_4)
        self.waitPosTable = QtGui.QTableWidget(self.waitPosTab)
        self.waitPosTable.setObjectName(_fromUtf8("waitPosTable"))
        self.waitPosTable.setColumnCount(0)
        self.waitPosTable.setRowCount(0)
        self.verticalLayout_3.addWidget(self.waitPosTable)
        self.TabWidget.addTab(self.waitPosTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.TabWidget)
        self.buttonBox = QtGui.QDialogButtonBox(StuffListDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(StuffListDialog)
        self.TabWidget.setCurrentIndex(0)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), StuffListDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), StuffListDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(StuffListDialog)
        StuffListDialog.setTabOrder(self.IdSpinBox, self.allStuffTable)
        StuffListDialog.setTabOrder(self.allStuffTable, self.workPosTable)
        StuffListDialog.setTabOrder(self.workPosTable, self.waitPosTable)
        StuffListDialog.setTabOrder(self.waitPosTable, self.buttonBox)
        StuffListDialog.setTabOrder(self.buttonBox, self.TabWidget)

    def retranslateUi(self, StuffListDialog):
        StuffListDialog.setWindowTitle(QtGui.QApplication.translate("StuffListDialog", "查看员工队列", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("StuffListDialog", "查看工作队列:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setToolTip(QtGui.QApplication.translate("StuffListDialog", "在表中快速定位该名员工", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("StuffListDialog", "员工工号:", None, QtGui.QApplication.UnicodeUTF8))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.allStuffTab), QtGui.QApplication.translate("StuffListDialog", "所有员工", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("StuffListDialog", "提示:下表序号是员工所在队列中所排序号(不是员工工号).", None, QtGui.QApplication.UnicodeUTF8))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.workPosTab), QtGui.QApplication.translate("StuffListDialog", "工作序号", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("StuffListDialog", "提示:下表序号是员工所在队列中所排序号(不是员工工号).", None, QtGui.QApplication.UnicodeUTF8))
        self.TabWidget.setTabText(self.TabWidget.indexOf(self.waitPosTab), QtGui.QApplication.translate("StuffListDialog", "等待序号", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    StuffListDialog = QtGui.QDialog()
    ui = Ui_StuffListDialog()
    ui.setupUi(StuffListDialog)
    StuffListDialog.show()
    sys.exit(app.exec_())

