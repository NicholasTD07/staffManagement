#!/usr/bin/python3
# File Info :
#   主窗口图表

# 系统 #
import sys

# PyQt #
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# 引用 #
import staffdata

# 错误 #
from errorclass import *


class StaffMenu(QMenu) :

    def __init__(self, staffs, staff, event, parent=None) :
        super(QMenu, self).__init__()
        # 获得员工 #
        self.staffs = staffs
        self.staff = staff
        self.Id = staff.Id
        # 获得员工函数 #
        self.staffWork = self.staffs.staffWork
        self.staffWait = self.staffs.staffWait
        # 获得工作类型 #
        self.NOR = self.staffs.NOR
        self.SEL = self.staffs.SEL
        self.NAMED = self.staffs.NAMED
        self.WAIT = self.staffs.WAIT
        # 添加动作 #
        self.norWorkAction = QAction("排钟", self)
        self.addAction(self.norWorkAction)
        self.selWorkAction = QAction("选钟", self)
        self.addAction(self.selWorkAction)
        self.namedWorkAction = QAction("点钟", self)
        self.addAction(self.namedWorkAction)
        self.addSeparator()
        self.waitAction = QAction("等待", self)
        self.addAction(self.waitAction)
        self.idleAction = QAction("下班", self)
        self.addAction(self.idleAction)
        # 连接动作和槽 #
        self.connectSlot(self.norWorkAction, self.norWork)
        self.connectSlot(self.selWorkAction, self.selWork)
        self.connectSlot(self.namedWorkAction, self.namedWork)
        self.connectSlot(self.waitAction, self.wait)
        self.exec(event.screenPos())

    def connectSlot(self, action=None, slot=None,
            signal="activated()") :
        if action is not None :
            if slot is not None:
                self.connect(action, SIGNAL(signal), slot)

    def norWork(self) :
        self.staffWork(self.Id, self.NOR)

    def selWork(self) :
        self.staffWork(self.Id, self.SEL)
        
    def namedWork(self) :
        self.staffWork(self.Id, self.NAMED)

    def wait(self) :
        print("StaffWait")
        self.staffWait(self.Id)


class StaffIcon(QGraphicsItem) :
    
    red, green, blue = 0, 0, 255
    WorkColor = QColor(red, green, blue)

    red, green, blue = 0, 255, 0 
    WaitColor = QColor(red, green, blue)

    Rect = QRectF(0, 0, 40, 40)

    def __init__(self, staffs, staff, parent) :
        super(StaffIcon, self).__init__()
        print("初始化 员工图标.员工序号: {}".format(staff.Id))
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

    def boundingRect(self) :
        return StaffIcon.Rect

    def paint(self, painter, option, widget=None):
        #painter.setPen(Qt.NoPen)
        print("员工图标 绘图.")
        painter.setBrush(QBrush(self.color))
        painter.drawRect(StaffIcon.Rect)

    def update(self) :
        self.putInPlace()
        QGraphicsItem.update(self, StaffIcon.Rect)
        
    def putInPlace(self) :
        print("员工图标 放置位置.")
        staff = self.staff
        wType = staff.wType
        if wType is self.staffs.WAIT :
            print("员工颜色为等待.")
            self.color = self.WaitColor
        elif wType in self.staffs.workTypes :
            print("员工颜色为工作.")
            self.color = self.WorkColor
        else :
            raise wrongType("类型错误({}), 不予画图."\
                .format(self.wType))
        self.wPos = self.workSeqs[staff.wTime].nSeq.index(staff)
        self.wTime = self.staff.wTime
        x = (self.wPos * 40)
        y = (self.wTime * 40)
        self.position = QPointF(x, y)
        if self.position != self.pos() :
            self.setPos(self.position)

    def contextMenuEvent(self, event) :
        Menu = StaffMenu(self.staffs, self.staff, event, self)
        self.parent.rerange()


class WorkGraph(QWidget) :
    
    SceneWidth = 1024
    SceneHeight = 600
    
    def __init__(self, staffs, parent=None) :
        super(WorkGraph, self).__init__(parent)
        self.staffs = staffs
        self.workGroup = staffs.getWorkGroup()


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

    def clear(self) :
        pass

    def populate(self) :
        # 初始化局部变量 #
        staffs = self.staffs
        getStaff = staffs.getStaff
        groups = staffs.getGroups()
        if self.workGroup is None :
            return
        workGroup = groups[self.workGroup]
        for Id in workGroup :
            staff = getStaff(Id)
            try :
                staffIcon = StaffIcon(self.staffs, staff, self)
            except wrongType :
                continue
            self.scene.addItem(staffIcon)

    def rerange(self) :
        scenes = self.view.scene()
        stafficons = [ item for item in scenes.items()
                        if isinstance(item, StaffIcon)]

        for stafficon in stafficons :
            stafficon.putInPlace()

        scenes.update(scenes.sceneRect())


if __name__ == '__main__' :
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
    S.staffsWait(1,2,3,4,5,6,7,8,9)
    # 测试 有选钟情况下的点钟.
    S.staffsWork(S.SEL, 1,2,3)
    S.reportStaffs()
    S.staffsWork(S.NAMED, 4)
    S.reportStaffs()
    # 测试存入文件

    form = WorkGraph(S)
    rect = QApplication.desktop().availableGeometry()
    form.resize(int(rect.width() * 0.75), int(rect.height() * 0.9))
    form.show()
    sys.exit(app.exec_())
