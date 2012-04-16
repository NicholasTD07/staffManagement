#!/usr/bin/python3
# File Info :
#   主窗口图表

# 系统 #
import sys

# PyQt #
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# 引用 #
#import staffdata

# 错误 #
from errorclass import *

class StaffIcon(QGraphicsItem) :
    
    red, green, blue = 0, 0, 255
    WorkColor = QColor(red, green, blue)

    red, green, blue = 0, 255, 0 
    WaitColor = QColor(red, green, blue)

    Rect = QRectF(-40, -40, 40, 40)

    def __init__(self, staffs, staff) :
        QGraphicsItem.__init__()
        self.staffs = staffs
        self.workSeqs = staffs.getWorkSeq()
        self.workTypes = staffs.workTypes
        self.putInPlace()

    def boundingRect(self) :
        return StaffIcon.Rect

    def paint(self, painter, option, widget=None):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.color))
        painter.drawRect(StaffIcon.Rect)

    def update(self) :
        self.putInPlace()
        QGraphicsItem.update(self, StaffIcon.Rect)
        
    def putInPlace(self) :
        if staff.wType is staffs.WAIT :
            self.color = WaitColor
        elif staff.wType is self.workTypes :
            self.color = WorkColor
        else :
            raise wrongType("类型错误, 不予画图.")
        self.wPos = self.workSeqs[staff.wTime].nSeq.index(staff)
        self.wTime = self.staff.wTime
        x = (self.wPos * 40)
        y = (self.wTime * 40)
        self.position = QPoint(x, y)
        self.setPos(self.position)
        


class WorkGraph(QWidget) :
    
    SceneWidth = 2000
    SceneHeight = 800
    
    def __init__(self, staffs, parent=None) :
        #QWidget.__init__(parent)
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

if __name__ is '__main__' :
    app = QApplication(sys.argv)
    form = WorkGraph()
    rect = QApplication.desktop().availableGeometry()
    form.resize(int(rect.width() * 0.75), int(rect.height() * 0.9))
    form.show()
    app.exec_()
