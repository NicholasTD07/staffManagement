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


class StaffIcon(QGraphicsItem) :
    
    red, green, blue = 0, 0, 255
    WorkColor = QColor(red, green, blue)

    red, green, blue = 0, 255, 0 
    WaitColor = QColor(red, green, blue)

    Rect = QRectF(0, 0, 40, 40)

    def __init__(self, staffs, staff) :
        super(StaffIcon, self).__init__()
        print("初始化 员工图标.员工序号: {}".format(staff.Id))
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
        if staff.wType is self.staffs.WAIT :
            self.color = self.WaitColor
        elif staff.wType is self.workTypes :
            self.color = self.WorkColor
        else :
            raise wrongType("类型错误, 不予画图.")
        self.wPos = self.workSeqs[staff.wTime].nSeq.index(staff)
        self.wTime = self.staff.wTime
        x = (self.wPos * 40)
        y = (self.wTime * 40)
        self.position = QPointF(x, y)
        self.setPos(self.position)



class WorkGraph(QWidget) :
    
    SceneWidth = 1024
    SceneHeight = 600
    
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

    def clear(self) :
        pass

    def populate(self) :
        for staff in self.staffs :
            try :
                staffIcon = StaffIcon(self.staffs, staff)
            except wrongType :
                continue
            self.scene.addItem(staffIcon)

    def update(self, staff) :
        # 1.remove
        # 2.add
        pass

if __name__ == '__main__' :
    app = QApplication(sys.argv)

    S = staffdata.StaffContainer()
    # 重建测试环境
    print()
    print()
    print()
    S.clear()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9,)
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
