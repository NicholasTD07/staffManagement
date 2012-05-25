#!/usr/bin/python3
# File Info :
#   主窗口程序


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
import shiftdialog


class MainWindow(QMainWindow) :


#{{{
    #{{{ #---- 初始化主窗口 ----# 
    def __init__(self, parent=None) : 
        # 1. 初始化 主窗口
        super(MainWindow, self).__init__(parent)
        self.staffs = staffdata.StaffContainer()
        self.log = self.staffs.log
        self.setupUi()

        #{{{ 2. 连接信号和槽
        self.connectSlot(self.fileNewAction, self.fileNew)
        self.connectSlot(self.fileOpenAction, self.fileOpen)
        self.connectSlot(self.fileSaveAction, self.fileSave)
        self.connectSlot(self.fileSaveAsAction, self.fileSaveAs)
        self.connectSlot(self.quitAction, self.close)
        self.connectSlot(self.staffAddAction, self.addStaff)
        self.connectSlot(self.staffDelAction, self.deleteStaff)
        self.connectSlot(self.groupStaffAction, self.groupStaff)
        self.connectSlot(self.shiftStaffAction, self.shiftGroup)
        self.connectSlot(self.listStaffAction, self.checkTable)
        #}}}

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
        QTimer.singleShot(0, self.initWorkGraph)
    #}}}

#{{{ # 设置界面 #
    def setupUi(self) :
        # 初始化主窗口 #
        self.resize(800, 600)

        # 菜单栏状态栏工具栏 #
        menuBar = QMenuBar(self)
        toolBar = QToolBar(self)
        statusBar = QStatusBar(self)
        # 设置属性 #
        menuBar.setObjectName("menuBar")
        toolBar.setObjectName("toolBar")
        statusBar.setObjectName("statusBar")
        # 挂入主窗口 #
        self.menuBar = menuBar
        self.toolBar = toolBar
        self.statusBar = statusBar

    #{{{ #-- 添加动作 --#

        #{{{ # 文件动作 #
        fileNewAction = QAction("新建文件(&N)", self)
        fileNewAction.setShortcut("Ctrl+N")
        fileOpenAction = QAction("打开文件(&O)", self)
        fileOpenAction.setShortcut("Ctrl+O")
        fileSaveAction = QAction("保存文件(&S)", self)
        fileSaveAction.setShortcut("Ctrl+S")
        fileSaveAsAction = QAction("另存为...(&A)", self)
        fileSaveAsAction.setShortcut("Ctrl+A")
        quitAction = QAction("退出程序(&Q)", self)
        quitAction.setShortcut("Ctrl+Q")
        # 挂入主窗口 #
        self.fileNewAction = fileNewAction
        self.fileOpenAction = fileOpenAction
        self.fileSaveAction = fileSaveAction
        self.fileSaveAsAction = fileSaveAsAction
        self.quitAction = quitAction
        #}}}

        #{{{ # 员工动作 #
        staffAddAction = QAction("增加员工(&I)", self)
        staffAddAction.setShortcut("Ctrl+I")
        staffDelAction = QAction("减少员工(&D)", self)
        staffDelAction.setShortcut("Ctrl+D")
        groupStaffAction = QAction("员工分组(&G)", self)
        groupStaffAction.setShortcut("Ctrl+G")
        shiftStaffAction = QAction("轮换班组(&C)", self)
        shiftStaffAction.setShortcut("Ctrl+C")
        listStaffAction = QAction("查看员工(&L)", self)
        listStaffAction.setShortcut("Ctrl+L")
        # 挂入主窗口 #
        self.staffAddAction = staffAddAction
        self.staffDelAction = staffDelAction
        self.groupStaffAction = groupStaffAction
        self.shiftStaffAction = shiftStaffAction
        self.listStaffAction = listStaffAction
        #}}}

        #{{{ #-- 添加菜单 --#
        fileMenu = QMenu("文件(&F)", menuBar)
        staffMenu = QMenu("管理员工(&M)", menuBar)
        # 挂入主窗口 #
        self.fileMenu = fileMenu
        self.staffMenu = staffMenu
        # 挂入菜单栏 #
        menuBar.addMenu(fileMenu)
        menuBar.addMenu(staffMenu)
        #}}}

        #{{{ #-- 添加动作 --#
        addFileAction = fileMenu.addAction
        addStaffAction = staffMenu.addAction
        addToolbarAction = toolBar.addAction
        # 文件菜单 #
        fileActions = [ fileNewAction, fileOpenAction, None,
                fileSaveAction, fileSaveAsAction, None, quitAction ]
        for action in fileActions :
            if action is None :
                fileMenu.addSeparator()
            else :
                addFileAction(action)
        # 员工菜单 #
        staffActions = [ staffAddAction, staffDelAction, None,
                groupStaffAction, shiftStaffAction, None, listStaffAction ]
        for action in staffActions :
            if action is None :
                staffMenu.addSeparator()
            else :
                addStaffAction(action)
        # 工具栏 #
        toolBarActions = [ fileOpenAction, fileSaveAction, None,
                staffAddAction, groupStaffAction, listStaffAction,
                None, quitAction ]
        for action in toolBarActions :
            if action is None :
                toolBar.addSeparator()
            else :
                addToolbarAction(action)
        #}}}
        
    #}}}

    #{{{ # 设置属性 #
        self.setMenuBar(menuBar)
        self.setStatusBar(statusBar)
        self.addToolBar(Qt.TopToolBarArea, toolBar)
    #}}}
#}}}

#{{{ #---- 重定义 ----#

    #{{{ 重定义: 关闭时 检查文件是否已保存
    #            并且 存入当前设置
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
    #}}}
#}}}

#{{{ #---- 窗口内部函数 ----#

    #{{{ # 连接 信号和槽 #
    def connectSlot(self, action=None, slot=None,
            signal="triggered()") :
        if action is not None :
            if slot is not None:
                self.connect(action, SIGNAL(signal), slot)
    #}}}

    #{{{ # 检查文件是否已保存 #
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
    #}}}

    #{{{ # 载入上次的文件 #
    def loadLastFile(self) :
        settings = QSettings()
        fileName = settings.value("LastFile")
        if fileName and QFile.exists(fileName) :
            ok, msg, staffs = self.staffs.load(fileName)
            self.staffs = staffs
            self.staffs.setDirty(False)
            self.statusBar.showMessage(msg, 5000)
    #}}}

    #{{{ # 初始化工作表 #
    def initWorkGraph(self) :
        workGraph = workgraph.WorkGraph(self.staffs, self)
        rect = QApplication.desktop().availableGeometry()
        workGraph.resize(int(rect.width() * 0.75), int(rect.height() * 0.9))
        self.workGraph = workGraph
        self.setCentralWidget(self.workGraph)
        # 7. 并设置为 主部件
    #}}}

    #{{{ # 关于 #
    def helpAbout(self):
        QMessageBox.about(self, "员工管理系统",
            """<b>员工信息管理 </b> v {0}
            <p>Python {1} - Qt {2} - PyQt {3} on {4}
            <p><b>作者: thedevil7<b>
            <p><b>Email: thedevil5032@gmail.com <b>""".format(
            __version__, platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR,
                platform.system()))
    #}}}
#}}}

#{{{ #---- 文件操作 ----#

    #{{{ # 新建文件 #
    def fileNew(self) :
        if not self.okToContinue() :
            return
        self.staffs.clear()
        self.statusBar.clearMessage()
        msg = "新建员工信息成功!"
        self.statusBar.showMessage(msg, 5000)
        self.initWorkGraph()
    #}}}

    #{{{ # 读取文件 #
    def fileOpen(self) :
        if not self.okToContinue() :
            return
        path = (QFileInfo(self.staffs.getFilename()).path()
                if self.staffs.getFilename() else ".")
        fileName = QFileDialog.getOpenFileName(self,
                        "员工信息: 导入数据", path,
                        "员工信息文件: ({})".format(
                                    self.staffs.fileFormats()))
        if fileName and QFile.exists(fileName) :
            ok, msg, staffs = self.staffs.load(fileName)
            if not ok :
                QMessageBox.information(self,
                            "读取文件: 失败.",
                            "读取文件出现异常错误:\n {}\n"\
                                .format(msg))
            self.staffs = staffs
            self.staffs.setDirty(False)
            self.statusBar.showMessage(msg, 5000)
            self.initWorkGraph()
    #}}}

    #{{{ # 保存文件 #
    def fileSave(self) :
        if not self.staffs.getFilename() :
            return self.fileSaveAs()
        else :
            ok, msg = self.staffs.save()
            self.statusBar.showMessage(msg, 5000)
            return ok
    #}}}

    #{{{ # 另存文件 #
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
            self.statusBar.showMessage(msg, 5000)
            return ok
        return False
    #}}}
#}}}

#{{{ #---- 员工操作 ----#

    #{{{ # 添加员工 #
    def addStaff(self) :
        form = updatestaffdialog.UpdateStaffDialog(
                    self.staffs, None, self)
        if form.exec_() :
            #self.updateSOMETHING()
            pass
    #}}}

    #{{{ # 删除员工 #
    def deleteStaff(self) :
        form = deletestaffdialog.DeleteStaffDialog(self.staffs,
                                                    None, self)
        if form.exec_() :
            #self.updateSOMETHING()
            pass
            #}}}

    #{{{ # 员工列表 #
    def checkTable(self) :
        form = stafflistdialog.StaffListDialog(
                    self.staffs, self)
        if form.exec_() :
            #self.updateSOMETHING()
            pass
    #}}}

    #{{{ # 员工分组 #
    def groupStaff(self) :
        form = groupstaffdialog.GroupStaffDialog(
                self.staffs, self)
        if form.exec() :
            print(self.staffs.getWorkSeq()[0].nSeq)
            self.workGraph.populate()
    #}}}

    #{{{ # 员工换班 #
    def shiftGroup(self) :
        form = shiftdialog.ShiftDialog(
                self.staffs, self)
        if form.exec() :
            self.workGraph.populate()
    #}}}
#}}}
#}}}

if __name__ == '__main__' :
    import sys
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())

