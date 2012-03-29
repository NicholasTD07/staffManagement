#!/usr/bin/python3
# File Info :
#   主窗口图表


import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import stuffdata


class StuffIcon(QGraphicsItem) :
    
    red, green, blue = 0, 0, 255
    WorkColor = QColor(red, green, blue)

    red, green, blue = 0, 255, 0 
    WaitColor = QColor(red, green, blue)

    Rect = QRectF(-40, -40, 40, 40)

    def __init__(self, stuff) :
        QGraphicsItem.__init__()
        self.stuff = stuff
        self.putInPlace()

    def boundingRect(self) :
        return StuffIcon.Rect

    def paint(self, painter, option, widget=None):
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(self.color))
        painter.drawRect(StuffIcon.Rect)

    def update(self) :
        self.putInPlace()
        QGraphicsItem.update(self, StuffIcon.Rect)
        
    def putInPlace(self) :
        if stuff.wType is stuffdata.StuffContainer.WAIT :
            self.color = WaitColor
            self.wPos = self.stuff.waitPos
            self.wTime = self.stuff.wTime
        elif stuff.wType is (stuffdata.StuffContainer.SEL or
                                stuffdata.StuffContainer.NOR or 
                                stuffdata.StuffContainer.NAMED ) :
            self.color = WorkColor
            self.wPos = self.stuff.workPos
            self.wTime = self.stuff.wTime

        else :
            return
        x = (self.wPos * 40)
        y = (self.wTime * 40)
        self.position = QPoint(x, y)
        self.setPos(self.position)
        


class WorkGraph(QWidget) :
    
    SceneWidth = 2000
    SceneHeight = 800
    
    def __init__(self, stuffs, parent=None) :
        #QWidget.__init__(parent)
        super(WorkGraph, self).__init__(parent)
        self.stuffs = stuffs


        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0,
                                self.SceneWidth, self.SceneHeight)
        #self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.view = QGraphicsView()
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setScene(self.scene)
        self.view.setFocusPolicy(Qt.NoFocus)

        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)

        #self.populate()

    def clear(self) :
        pass

    def populate(self) :
        for stuff in self.stuffs :
            stuffIcon = StuffIcon(stuff)
            self.scene.addItem(stuffIcon)

    def update(self, stuff) :
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


