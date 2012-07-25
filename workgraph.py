#!/usr/bin/python3
# File Info :
#   主窗口图表

#    Copyright 2012 Nicholas Tian

#    This file is part of Staff Management Project.
#
#    Staff Management Project is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Straff Management Project is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Straff Management Project.  If not, see <http://www.gnu.org/licenses/>.


# PyQt #
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# 引用 #
import staffdata

# 错误 #
from errorclass import *


class StaffIcon(QGraphicsItem) :


    "This is the Icon in the workgraph for every working staff."
    
    red, green, blue = 0, 0, 255
    WorkColor = QColor(red, green, blue)

    red, green, blue = 0, 255, 0 
    WaitColor = QColor(red, green, blue)

    Rect = QRectF(0, 0, 40, 40)


    #---- Initialize the StaffIcon ----#
    def __init__(self, staffs, staff, parent) :
        # Get log #
        log = staffs.log
        log("StaffIcon - init ---- Start.")
        self.log = log
        # Initialize parent #
        super(StaffIcon, self).__init__()
        # Get parent and its rerange function, staff, staffs #
        self.Id = staff.Id
        self.staff = staff
        self.staffs = staffs
        self.rerange = parent.rerange
        log("StaffIcon - init - Fetched parent, staff, staffs.")
        # Get workSeqs and workTypes #
        self.workSeqs = staffs.getWorkSeq()
        self.workTypes = staffs.workTypes
        log("StaffIcon - init - Fetched workSeqs and workTypes.")
        # Place this icon where it should be #
        log("StaffIcon - init - Run into putInPlace().")
        self.putInPlace()
        # Set the number inside this icon #
        log("StaffIcon - init - Setup number in the icon.")
        self.StaffNum = QGraphicsTextItem("{}"\
                .format(self.Id), self)
        self.StaffNum.setTextWidth(10)
        self.StaffNum.setFont(QFont("Times", 20))
        self.StaffNum.adjustSize()
        # The End #
        log("StaffIcon - init ---- End.\n\n")


    def boundingRect(self) :
        return StaffIcon.Rect


    def paint(self, painter, option, widget=None):
        painter.setBrush(QBrush(self.color))
        painter.drawRect(StaffIcon.Rect)


    def update(self) :
        self.putInPlace()
        QGraphicsItem.update(self, StaffIcon.Rect)


    # Setup where it is and how does it look like #
    def putInPlace(self) :
        # Get log #
        log = self.log
        log("StaffIcon - putInPlace ---- Start.")
        # Get staff and his worktype #
        staff = self.staff
        wType = staff.wType
        log("StaffIcon - putInPlace - Fetched staff and his worktype")
        if wType == self.staffs.WAIT :
            self.color = self.WaitColor
            log("StaffIcon - putInPlace - Use WaitColor.")
        elif wType in self.staffs.workTypes :
            self.color = self.WorkColor
            log("StaffIcon - putInPlace - Use WorkColor.")
        else :
            log("StaffIcon - putInPlace ---- OOPS, wrong type.")
            self.scene().removeItem(self)
            raise wrongType("类型错误({}), 不予画图."\
                .format(wType))
        log("\nStaffIcon - putInPlace - Call staff.tell.\n\t" + staff.tell() + "\n")
        self.wPos = self.workSeqs[staff.wTime].nSeq.index(staff)
        self.wTime = self.staff.wTime
        x = (self.wPos * 40)
        y = (self.wTime * 40)
        self.position = QPointF(x, y)
        log("StaffIcon - putInPlace - Fetched work position and calculated position in WorkGraph.")
        if self.position != self.pos() :
            self.setPos(self.position)
            log("StaffIcon - putInPlace - Positon Changed.")
        log("StaffIcon - putInPlace ---- End.\n\n")


    def contextMenuEvent(self, event) :
        # Get log #
        log = self.log
        log("StaffIcon - contextMenuEvent ---- Start.")
        # Create Menu #
        StaffMenu = QMenu()
        # Get Staff #
        Id = self.Id
        staff = self.staff
        wType = staff.wType
        log("\tStaff Id: {}, name: {}, gender: {}, workType: {}".format(Id,
            staff.name, staff. gender, wType))
        staffs = self.staffs
        staffWork = staffs.staffWork
        log("StaffIcon - contextMenuEvent - Fetched Id, staff, staffs, staffWork.")
        # Create actions and connect them #
        if wType == staffs.WAIT :
            log("StaffMenu - contextMenuEvent - Staff is waiting.")
            norWorkAction = StaffMenu.addAction("排钟")
            selWorkAction = StaffMenu.addAction("选种")
            namedWorkAction = StaffMenu.addAction("点钟")
            StaffMenu.addSeparator()
            idleAction = StaffMenu.addAction("下班")
            norWorkAction.triggered.connect( lambda : staffWork(Id, staffs.NOR) )
            selWorkAction.triggered.connect( lambda : staffWork(Id, staffs.SEL) )
            namedWorkAction.triggered.connect( lambda : staffWork(Id, staffs.NAMED) )
            idleAction.triggered.connect( lambda : staffs.staffIdle(Id) )
            log("StaffMenu - contextMenuEvent - Created nor, sel, named, idle actions.")
        elif wType in staffs.workTypes :
            log("StaffMenu - contextMenuEvent - Staff is working.")
            waitAction = StaffMenu.addAction("等待")
            waitAction.triggered.connect( lambda : staffs.staffWait(Id) )
            log("StaffMenu - contextMenuEvent - Created wait action.")
        action = StaffMenu.exec(event.screenPos())
        if action is not None :
            log("StaffIcon - contextMenuEvent ---- Excuted.")
            log("StaffIcon - contextMenuEvent - Call WorkGraph's rerange().\n\n")
            self.rerange()
        else :
            log("StaffIcon - contextMenuEvent - Gave up.")


class WorkGraph(QWidget) :
    
    SceneWidth = 1024
    SceneHeight = 600
    
    # Initialize the WorkGraph in mainwindow #
    def __init__(self, staffs, parent=None) :
        # Get log #
        log = staffs.log
        self.log = log
        log("WorkGraph - init ---- Start.")
        # Initialize parent #
        super(WorkGraph, self).__init__(parent)
        # Get staffs #
        self.staffs = staffs
        log("WorkGraph - init - Fetched staffs.")
        # Setup the scene and view #
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0,
                        self.SceneWidth, self.SceneHeight)
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.view = QGraphicsView()
        self.view.setRenderHint(QPainter.Antialiasing)
        self.view.setScene(self.scene)
        self.view.setFocusPolicy(Qt.NoFocus)
        log("WorkGraph - init - Set up everything for scene and view in this WorkGraph.")
        # Setup layout #
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        self.setLayout(layout)
        log("WorkGraph - init - Set up layout.")
        # Populate icons for every staff #
        log("WorkGraph - init - Call populate() to populate icons for staffs.")
        self.populate()
        log("WorkGraph - init - Show the view.")
        self.view.show()
        log("WorkGraph - init ---- End.\n\n")


    # Populate icons #
    def populate(self) :
        # Get log #
        log = self.log
        log("WorkGraph - populate ---- Start.")
        # Clean the scene #
        log("WorkGraph - populate - Clean the scene.")
        self.scene.clear()
        # Get staffs, workSeqs, and getStaff() #
        staffs = self.staffs
        getStaff = staffs.getStaff
        workSeqs = staffs.getWorkSeq()
        log("WorkGraph - populate - Fetched staffs, workSeqs, and getStaff().")
        log("WorkGraph -- populate - Entering for loop to go over every workSeq in workSeqs.\n")
        for workSeq in workSeqs :
            nSeq = workSeq.nSeq
            log("WorkGraph -- populate - Go over every staff which is not None in every workSeq in a for loop.\n")
            for staff in nSeq :
                if staff is None :
                    log("WorkGraph - populate - Staff is None. Next staff.")
                    continue
                try :
                    log("WorkGraph - populate - Staff is not None. Get a icon for him or her.\n")
                    staffIcon = StaffIcon(self.staffs, staff, self)
                except wrongType :
                    log("WorkGraph - populate - Staff has a wrong worktype.")
                    continue
                self.scene.addItem(staffIcon)
                log("WorkGraph - populate - Add this icon into WorkGraph.\n")
            log("WorkGraph - populate ---- End.\n\n")


    # Rerange icons in the scene #
    def rerange(self) :
        # Get log #
        log = self.log
        log("WorkGraph - rerange ---- Start.")
        # Get scenes in the view and get every icon #
        log("WorkGraph - rerange - Get scenes in the view and get every icon.")
        scenes = self.view.scene()
        stafficons = [ item for item in scenes.items()
                        if isinstance(item, StaffIcon)]
        # Replace icon if needed #
        log("WorkGraph - rerange - Go into a for loop. Replace icons if needed.\n")
        for stafficon in stafficons :
            try :
                log("WorkGraph - rerange - Call icons' putInPlace().")
                stafficon.putInPlace()
            except wrongType :
                log("WorkGraph - rerange - Not calling icons' putInPlace() for staff's wrong worktype.")
                continue
        log("WorkGraph - rerange - Update the whole scene.")
        scenes.update(scenes.sceneRect())
        log("WorkGraph - rerange ---- End.\n\n")

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
    S.groupStaff(4,1)
    S.groupStaff(5,1)
    S.groupStaff(6,1)
    S.groupStaff(7,1)
    S.groupStaff(8,1)
    S.groupStaff(9,1)
    S.shiftStaff(1)
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
