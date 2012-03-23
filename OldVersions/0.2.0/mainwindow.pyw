#!/usr/bin/python3
# File Info :
#   主窗口程序

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import stuffdata
import updatestuffdialog_idlineedit
import stufflistdialog_tabwidget
import deletestuffdialog
import workgraph
import ui_mainwindow


__version__ = "0.1.1"


class MainWindow(QMainWindow,
        ui_mainwindow.Ui_MainWindow) :
    
    def __init__(self, parent=None) :
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        self.stuffs = stuffdata.StuffContainer()
        self.connectSlot(self.fileNewAction, self.fileNew)
        self.connectSlot(self.fileOpenAction, self.fileOpen)
        self.connectSlot(self.fileSaveAction, self.fileSave)
        self.connectSlot(self.fileSaveAsAction, self.fileSaveAs)
        self.connectSlot(self.fileQuitAction, self.close)
        self.connectSlot(self.addStuffAction, self.addStuff)
        self.connectSlot(self.deleteStuffAction,
                                    self.deleteStuff)
        self.connectSlot(self.checkTableAction,
                                    self.checkTable)
                                    

        settings = QSettings()
        self.restoreGeometry(
                settings.value("MainWindow/Geometry",
                                QByteArray()))
        self.restoreState(
                settings.value("MainWindow/State",
                                QByteArray()))

        self.setWindowTitle("员工信息管理系统")

        QTimer.singleShot(0, self.loadLastFile)

        self.workGraph = workgraph.WorkGraph(self.stuffs, self)
        self.setCentralWidget(self.workGraph)

    def closeEvent(self, event) :
        if self.okToContinue() :
            settings = QSettings()
            settings.setValue("LastFile",
                        self.stuffs.getFilename())
            settings.setValue("MainWindow/Geometry",
                        self.saveGeometry())
            settings.setValue("MainWindow/State",
                        self.saveState())
        else :
            event.ignore()

    def modifyAction(self,action=None, slot=None, shortcut=None,
            icon=None, tip=None, checkable=False,
            signal="triggered()") :
        if action is not None :
            if slot is not None:
                self.connect(action, SIGNAL(signal), slot)
            if shortcut is not None:
                action.setShortcut(shortcut)
            if icon is not None:
                action.setIcon(QIcon(":/{}.png".format(icon)))
            if tip is not None:
                action.setToolTip(tip)
                action.setStatusTip(tip)
            if checkable:
                action.setCheckable(True)

    def connectSlot(self, action=None, slot=None,
            signal="triggered()") :
        if action is not None :
            if slot is not None:
                self.connect(action, SIGNAL(signal), slot)
            
    def okToContinue(self) :
        if self.stuffs.isDirty() :
            reply = QMessageBox.question(self,
                    "员工信息: 尚未保存",
                    "现在保存员工信息?",
                    QMessageBox.Yes|QMessageBox.No\
                    |QMessageBox.Cancel)
            if reply == QMessageBox.Cancel :
                return False
            elif reply == QMessageBox.Yes :
                return self.fileSave()
        return True

    def graphUpdate(self, stuff) :
        self.workGraph.update(stuff)

    def graphPopulate(self) :
        self.workGraph.populate()

    def loadLastFile(self) :
        settings = QSettings()
        fileName = settings.value("LastFile")
        if fileName and QFile.exists(fileName) :
            ok, msg, stuffs = self.stuffs.load(fileName)
            self.stuffs = stuffs
            self.stuffs.setDirty(False)
            self.statusBar().showMessage(msg, 5000)
        #self.updateSOMETHING()
        self.graphPopulate()

    def fileNew(self) :
        if not self.okToContinue() :
            return
        self.stuffs.clear()
        self.statusBar().clearMessage()
        msg = "新建员工信息成功!"
        self.statusBar().showMessage(msg, 5000)
        #self.updateSOMETHING()
        self.workGraph.clear()

    def fileOpen(self) :
        if not self.okToContinue() :
            return
        path = (QFileInfo(self.stuffs.getFilename()).path()
                if self.stuffs.getFilename() else ".")
        fileName = QFileDialog.getOpenFileName(self,
                    "员工信息: 导入数据", path,
                    "员工信息文件: ({})".format(
                                    self.stuffs.fileFormats()))
        if fileName :
            ok, msg, stuffs = self.stuffs.load(fileName)
            self.stuffs = stuffs
            self.stuffs.setDirty(False)
            self.statusBar().showMessage(msg, 5000)
            #self.updateSOMETHING()
            self.graphPopulate()

    def fileSave(self) :
        if not self.stuffs.getFilename() :
            return self.fileSaveAs()
        else :
            ok, msg = self.stuffs.save()
            self.statusBar().showMessage(msg, 5000)
            return ok

    def fileSaveAs(self) :
        fileName = self.stuffs.getFilename()\
                    if self.stuffs.getFilename() else "."
        fileName = QFileDialog.getSaveFileName(self,
                    "员工信息: 保存数据", fileName,
                    "员工信息文件 ({})".format(
                                    self.stuffs.fileFormats()))
        if fileName :
            if "." not in fileName :
                fileName += ".qpc"
            ok, msg = self.stuffs.save(fileName)
            self.statusBar().showMessage(msg, 5000)
            return ok
        return False

    def addStuff(self) :
        form = updatestuffdialog_idlineedit.UpdateStuffDialog(
                    self.stuffs, None, self)
        if form.exec_() :
            #self.updateSOMETHING()
            pass

    def deleteStuff(self) :
        form = deletestuffdialog.DeleteStuffDialog(self.stuffs,
                                                    None, self)
        if form.exec_() :
            #self.updateSOMETHING()
            pass
            
    def checkTable(self) :
        form = stufflistdialog_tabwidget.StuffListDialog(
                    self.stuffs, self)
        if form.exec_() :
            #self.updateSOMETHING()
            pass

    def helpAbout(self):
        QMessageBox.about(self, "My Movies - About",
            """<b>员工信息管理 </b> v {0}
            <p>Python {1} - Qt {2} - PyQt {3} on {4}""".format(
            __version__, platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR,
                platform.system()))

if __name__ == '__main__' :
    import sys
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())

