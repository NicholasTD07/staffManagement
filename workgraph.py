#!/usr/bin/python3
# File Info :
#   主窗口图表


# PyQt #
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# 引用 #
import staffdata

# 错误 #
from errorclass import *


class StaffMenu(QMenu) :


#{{{ 员工菜单
#{{{ #---- 初始化员工菜单 ----#
    def __init__(self, staffs, staff, event, parent=None) :
        super(QMenu, self).__init__()
        # 获得员工 #
        self.staffs = staffs
        self.staff = staff
        self.Id = staff.Id
        # 获得员工函数 #
        self.staffWork = self.staffs.staffWork
        self.staffWait = self.staffs.staffWait
        self.staffIdle = self.staffs.staffIdle
        # 获得工作类型 #
        self.NOR = self.staffs.NOR
        self.SEL = self.staffs.SEL
        self.NAMED = self.staffs.NAMED
        self.WAIT = self.staffs.WAIT
        self.IDLE = self.staffs.IDLE
        # 添加动作 #
        self.norWorkAction = QAction("排钟", self)
        self.selWorkAction = QAction("选钟", self)
        self.namedWorkAction = QAction("点钟", self)
        self.waitAction = QAction("等待", self)
        self.idleAction = QAction("下班", self)
        # 更新菜单 #
        self.updateMenu()
        # 连接动作和槽 #
        self.connect(self.norWorkAction, SIGNAL("activated()"),
                #lambda : self.staffWork(self.Id, self.NOR))
                lambda : self.errorDetect(self.NOR))
        self.connect(self.selWorkAction, SIGNAL("activated()"),
                #lambda : self.staffWork(self.Id, self.SEL))
                lambda : self.errorDetect(self.SEL))
        self.connect(self.namedWorkAction, SIGNAL("activated()"),
                #lambda : self.staffWork(self.Id, self.NAMED))
                lambda : self.errorDetect(self.NAMED))
        self.connect(self.waitAction, SIGNAL("activated()"),
                #lambda : self.staffWait(self.Id))
                lambda : self.errorDetect(self.WAIT))
        self.connect(self.idleAction, SIGNAL("activated()"),
                #lambda : self.staffIdle(self.Id))
                lambda : self.errorDetect(self.IDLE))
        self.exec(event.screenPos())
#}}}

    #{{{ # 提供错误提醒 #
    def errorDetect(self, wType) :
        NOR = self.NOR
        SEL = self.SEL
        WAIT = self.WAIT
        IDLE = self.IDLE
        NAMED = self.NAMED
        try :
            if wType == NOR :
                self.staffWork(self.Id, NOR)
            elif wType == SEL :
                self.staffWork(self.Id, SEL)
            elif wType == NAMED :
                self.staffWork(self.Id, NAMED)
            elif wType == WAIT :
                self.staffWait(self.Id)
            elif wType == IDLE :
                self.staffIdle(self.Id)
            else :
                QMessageBox.warning(self,
                        "状态错误",
                        "出现未知状态.")
            # 更新菜单 #
            self.updateMenu()
        except Exception as e:
            QMessageBox.warning(self,
                    "错误",
                    str(e))
        #}}}

    def updateMenu(self) :
        self.clear()
        wType = self.staff.wType
        workTypes = self.staffs.workTypes
        if wType == self.WAIT :
            self.addAction(self.norWorkAction)
            self.addAction(self.selWorkAction)
            self.addAction(self.namedWorkAction)
            self.addSeparator()
            self.addAction(self.idleAction)
        elif wType in workTypes :
            self.addAction(self.waitAction)

#}}}


class StaffIcon(QGraphicsItem) :


#{{{ 员工图标
#{{{ # 初始化共用参数 #
    red, green, blue = 0, 0, 255
    WorkColor = QColor(red, green, blue)

    red, green, blue = 0, 255, 0 
    WaitColor = QColor(red, green, blue)

    Rect = QRectF(0, 0, 40, 40)
#}}}

#{{{ #---- 初始化员工图标 ----#
    def __init__(self, staffs, staff, parent) :
        super(StaffIcon, self).__init__()
        self.parent = parent
        self.staffs = staffs
        self.staff = staff
        self.Id = staff.Id
        self.workSeqs = staffs.getWorkSeq()
        self.workTypes = staffs.workTypes
        self.putInPlace()
        self.StaffNum = QGraphicsTextItem("{}"\
                .format(self.Id), self)
        self.StaffNum.setTextWidth(10)
        self.StaffNum.setFont(QFont("Times", 20))
        self.StaffNum.adjustSize()
#}}}

    def boundingRect(self) :
        return StaffIcon.Rect

    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(self.color))
        painter.drawRect(StaffIcon.Rect)

    def update(self) :
        self.putInPlace()
        QGraphicsItem.update(self, StaffIcon.Rect)

    #{{{ # 设置位置颜色 #
    def putInPlace(self) :
        staff = self.staff
        wType = staff.wType
        if wType == self.staffs.WAIT :
            self.color = self.WaitColor
        elif wType in self.staffs.workTypes :
            self.color = self.WorkColor
        else :
            self.scene().removeItem(self)
            raise wrongType("类型错误({}), 不予画图."\
                .format(wType))
        self.wPos = self.workSeqs[staff.wTime].nSeq.index(staff)
        self.wTime = self.staff.wTime
        x = (self.wPos * 40)
        y = (self.wTime * 40)
        self.position = QPointF(x, y)
        if self.position != self.pos() :
            self.setPos(self.position)
    #}}}

    def contextMenuEvent(self, event) :
        Menu = StaffMenu(self.staffs, self.staff, event, self)
        self.parent.rerange()
#}}}


class WorkGraph(QWidget) :
    
    SceneWidth = 1024
    SceneHeight = 600
    
#{{{ #---- 初始化员工图表 ----#
    def __init__(self, staffs, parent=None) :
        super(WorkGraph, self).__init__(parent)
        self.staffs = staffs

        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0,
                        self.SceneWidth, self.SceneHeight)
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.view = QGraphicsView()
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setScene(self.scene)
        self.view.setFocusPolicy(Qt.NoFocus)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.populate()

        self.view.show()
#}}}

    #{{{ # 更新图像 #
    def populate(self) :
        # 初始化局部变量 #
        self.scene.clear()
        staffs = self.staffs
        getStaff = staffs.getStaff
        groups = staffs.getGroups()
        workGroupNum = staffs.getWorkGroup()
        if workGroupNum is None :
            return
        workGroup = groups[workGroupNum]
        for Id in workGroup :
            staff = getStaff(Id)
            try :
                staffIcon = StaffIcon(self.staffs, staff, self)
            except wrongType :
                continue
            self.scene.addItem(staffIcon)
    #}}}

    #{{{ # 重新排位 #
    def rerange(self) :
        scenes = self.view.scene()
        stafficons = [ item for item in scenes.items()
                        if isinstance(item, StaffIcon)]

        for stafficon in stafficons :
            try :
                stafficon.putInPlace()
            except wrongType :
                continue
        scenes.update(scenes.sceneRect())
    #}}}

if __name__ == '__main__' :
    import sys

    app = QApplication(sys.argv)

    S = staffdata.StaffContainer()
    # 重建测试环境
    print()
    print()
    print()
    S.clear()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9,)
    S.groupStaff(1,1)
    S.groupStaff(2,1)
    S.groupStaff(3,1)
    S.setWorkGroup(1)
    S.reportStaffs()
    #S.staffsWait(1,2,3,4,5,6,7,8,9)
    ## 测试 有选钟情况下的点钟.
    #S.staffsWork(S.SEL, 1,2,3)
    #S.reportStaffs()
    #S.staffsWork(S.NAMED, 4)
    #S.reportStaffs()
    ## 测试存入文件

    form = WorkGraph(S)
    rect = QApplication.desktop().availableGeometry()
    form.resize(int(rect.width() * 0.75), int(rect.height() * 0.9))
    form.show()
    sys.exit(app.exec_())
