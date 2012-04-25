#!/usr/bin/python3
# File Info :
#   主窗口程序

# 系统 #
import sys

# PyQt #
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# 调用 #
import staffdata
import updatestaffdialog
import stafflistdialog
import deletestaffdialog
import workgraph
import groupstaffdialog

# 主窗口 UI #
import ui_mainwindow


__version__ = "0.3.0"


class MainWindow(QMainWindow, ui_mainwindow.Ui_MainWindow) :

    def __init__(self, parent=None) : 
        # 1. 初始化 主窗口
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)

        # 2. 连接信号和槽
        self.staffs = staffdata.StaffContainer()
        self.connectSlot(self.fileNewAction, self.fileNew)
        self.connectSlot(self.fileOpenAction, self.fileOpen)
        self.connectSlot(self.fileSaveAction, self.fileSave)
        self.connectSlot(self.fileSaveAsAction, self.fileSaveAs)
        self.connectSlot(self.fileQuitAction, self.close)
        self.connectSlot(self.addStaffAction, self.addStaff)
        self.connectSlot(self.groupStaffAction, self.groupStaff)
        self.connectSlot(self.deleteStaffAction,
                self.deleteStaff)
        self.connectSlot(self.checkTableAction,
                self.checkTable)
             
        # 3. 初始化 设置
        #    并且恢复上一次的窗口大小, 位置, 状态.
        settings = QSettings()
        self.restoreGeometry(settings.value("MainWindow/Geometry",
                                QByteArray()))
        self.restoreState(settings.value("MainWindow/State",
                                QByteArray()))

        # 4. 设置 窗口标题
        self.setWindowTitle("员工信息管理系统")
        # 5. 载入 上次的文件
        QTimer.singleShot(0, self.loadLastFile)
        # 6. 初始化 workGraph
        self.workGraph = workgraph.WorkGraph(self.staffs, self)
        # 7. 并设置为 主部件
        self.setCentralWidget(self.workGraph)

    #---- 重定义 ----#

    # 重定义: 关闭时 检查文件是否已保存
    #         并且 存入当前设置
    def closeEvent(self, event) :
        if self.okToContinue() :
            settings = QSettings()
            settings.setValue("LastFile",
                        self.staffs.getFilename())
            settings.setValue("MainWindow/Geometry",
                        self.saveGeometry())
            settings.setValue("MainWindow/State",
                        self.saveState())
        else :
            event.ignore()

    #---- 窗口内部函数 ----#

    # 连接 信号和槽 #
    def connectSlot(self, action=None, slot=None,
            signal="triggered()") :
        if action is not None :
            if slot is not None:
                self.connect(action, SIGNAL(signal), slot)

    # 检查文件是否已保存 #
    def okToContinue(self) :
        if self.staffs.isDirty() :
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

    # 载入上次的文件 #
    def loadLastFile(self) :
        settings = QSettings()
        fileName = settings.value("LastFile")
        if fileName and QFile.exists(fileName) :
            ok, msg, staffs = self.staffs.load(fileName)
            self.staffs = staffs
            self.staffs.setDirty(False)
            self.statusBar().showMessage(msg, 5000)
        #self.updateSOMETHING()

    # 关于 #
    def helpAbout(self):
        QMessageBox.about(self, "员工福安里系统",
            """<b>员工信息管理 </b> v {0}
            <p>Python {1} - Qt {2} - PyQt {3} on {4}
            <p><b>作者: thedevil7<b>
            <p><b>Email: thedevil5032@gmail.com <b>""".format(
            __version__, platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR,
                platform.system()))

    #---- 文件操作 ----#

    # 新建文件 #
    def fileNew(self) :
        if not self.okToContinue() :
            return
        self.staffs.clear()
        self.statusBar().clearMessage()
        msg = "新建员工信息成功!"
        self.statusBar().showMessage(msg, 5000)
        #self.updateSOMETHING()

    # 读取文件 #
    def fileOpen(self) :
        if not self.okToContinue() :
            return
        path = (QFileInfo(self.staffs.getFilename()).path()
                if self.staffs.getFilename() else ".")
        fileName = QFileDialog.getOpenFileName(self,
                        "员工信息: 导入数据", path,
                        "员工信息文件: ({})".format(
                                    self.staffs.fileFormats()))
        if fileName :
            ok, msg, staffs = self.staffs.load(fileName)
            if not ok :
                QMessageBox.information(self,
                            "读取文件: 失败.",
                            "读取文件出现异常错误:\n {}\n"\
                                .format(msg))
            self.staffs = staffs
            self.staffs.setDirty(False)
            self.statusBar().showMessage(msg, 5000)
            #self.updateSOMETHING()

    def fileSave(self) :
        if not self.staffs.getFilename() :
            return self.fileSaveAs()
        else :
            ok, msg = self.staffs.save()
            self.statusBar().showMessage(msg, 5000)
            return ok

    def fileSaveAs(self) :
        fileName = self.staffs.getFilename()\
                    if self.staffs.getFilename() else "."
        fileName = QFileDialog.getSaveFileName(self,
                    "员工信息: 保存数据", fileName,
                    "员工信息文件 ({})".format(
                                    self.staffs.fileFormats()))
        if fileName :
            if "." not in fileName :
                fileName += ".qpc"
            ok, msg = self.staffs.save(fileName)
            self.statusBar().showMessage(msg, 5000)
            return ok
        return False

    #---- 员工操作 ----#

    # 添加员工 #
    def addStaff(self) :
        form = updatestaffdialog.UpdateStaffDialog(
                    self.staffs, None, self)
        if form.exec_() :
            #self.updateSOMETHING()
            pass

    # 删除员工 #
    def deleteStaff(self) :
        form = deletestaffdialog.DeleteStaffDialog(self.staffs,
                                                    None, self)
        if form.exec_() :
            #self.updateSOMETHING()
            pass
            
    # 员工列表 #
    def checkTable(self) :
        form = stafflistdialog.StaffListDialog(
                    self.staffs, self)
        if form.exec_() :
            #self.updateSOMETHING()
            pass

    # 员工分组 #
    def groupStaff(self) :
        form = groupstaffdialog.GroupStaffDialog(
                self.staffs, self)
        if form.exec() :
            #self.updateSOMETHING()
            pass

if __name__ == '__main__' :
    import sys
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())

