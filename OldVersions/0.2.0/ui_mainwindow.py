# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_mainwindow.ui'
#
# Created: Mon Mar 12 08:43:53 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.fileMenu = QtGui.QMenu(self.menubar)
        self.fileMenu.setObjectName(_fromUtf8("fileMenu"))
        self.stuffMenu = QtGui.QMenu(self.menubar)
        self.stuffMenu.setObjectName(_fromUtf8("stuffMenu"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.fileSaveAction = QtGui.QAction(MainWindow)
        self.fileSaveAction.setObjectName(_fromUtf8("fileSaveAction"))
        self.fileOpenAction = QtGui.QAction(MainWindow)
        self.fileOpenAction.setObjectName(_fromUtf8("fileOpenAction"))
        self.addStuffAction = QtGui.QAction(MainWindow)
        self.addStuffAction.setObjectName(_fromUtf8("addStuffAction"))
        self.checkTableAction = QtGui.QAction(MainWindow)
        self.checkTableAction.setObjectName(_fromUtf8("checkTableAction"))
        self.fileQuitAction = QtGui.QAction(MainWindow)
        self.fileQuitAction.setObjectName(_fromUtf8("fileQuitAction"))
        self.fileNewAction = QtGui.QAction(MainWindow)
        self.fileNewAction.setObjectName(_fromUtf8("fileNewAction"))
        self.fileSaveAsAction = QtGui.QAction(MainWindow)
        self.fileSaveAsAction.setObjectName(_fromUtf8("fileSaveAsAction"))
        self.deleteStuffAction = QtGui.QAction(MainWindow)
        self.deleteStuffAction.setObjectName(_fromUtf8("deleteStuffAction"))
        self.fileMenu.addAction(self.fileNewAction)
        self.fileMenu.addAction(self.fileOpenAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.fileSaveAction)
        self.fileMenu.addAction(self.fileSaveAsAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.fileQuitAction)
        self.stuffMenu.addAction(self.addStuffAction)
        self.stuffMenu.addAction(self.deleteStuffAction)
        self.stuffMenu.addSeparator()
        self.stuffMenu.addAction(self.checkTableAction)
        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.stuffMenu.menuAction())
        self.toolBar.addAction(self.fileOpenAction)
        self.toolBar.addAction(self.fileSaveAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.addStuffAction)
        self.toolBar.addAction(self.checkTableAction)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.fileQuitAction)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.fileMenu.setTitle(QtGui.QApplication.translate("MainWindow", "文件(&F)", None, QtGui.QApplication.UnicodeUTF8))
        self.stuffMenu.setTitle(QtGui.QApplication.translate("MainWindow", "管理员工(&M)", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.fileSaveAction.setText(QtGui.QApplication.translate("MainWindow", "保存(&S)", None, QtGui.QApplication.UnicodeUTF8))
        self.fileSaveAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.fileOpenAction.setText(QtGui.QApplication.translate("MainWindow", "打开(&O)", None, QtGui.QApplication.UnicodeUTF8))
        self.fileOpenAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.addStuffAction.setText(QtGui.QApplication.translate("MainWindow", "添加员工(&I)", None, QtGui.QApplication.UnicodeUTF8))
        self.addStuffAction.setToolTip(QtGui.QApplication.translate("MainWindow", "添加员工(I)", None, QtGui.QApplication.UnicodeUTF8))
        self.addStuffAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+I", None, QtGui.QApplication.UnicodeUTF8))
        self.checkTableAction.setText(QtGui.QApplication.translate("MainWindow", "查看员工队列(&U)", None, QtGui.QApplication.UnicodeUTF8))
        self.checkTableAction.setToolTip(QtGui.QApplication.translate("MainWindow", "查看员工队列(&U)", None, QtGui.QApplication.UnicodeUTF8))
        self.checkTableAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+U", None, QtGui.QApplication.UnicodeUTF8))
        self.fileQuitAction.setText(QtGui.QApplication.translate("MainWindow", "退出(&Q)", None, QtGui.QApplication.UnicodeUTF8))
        self.fileQuitAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.fileNewAction.setText(QtGui.QApplication.translate("MainWindow", "新建(&N)", None, QtGui.QApplication.UnicodeUTF8))
        self.fileNewAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.fileSaveAsAction.setText(QtGui.QApplication.translate("MainWindow", "另存为(&A)", None, QtGui.QApplication.UnicodeUTF8))
        self.fileSaveAsAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+A", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteStuffAction.setText(QtGui.QApplication.translate("MainWindow", "删除员工(&D)", None, QtGui.QApplication.UnicodeUTF8))
        self.deleteStuffAction.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+D", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

