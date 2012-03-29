#!/usr/bin/python3
# File Info :
#   查看员工队列对话框

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import stuffdata
import ui_stufflistdialog_tabwidget
import updatestuffdialog_idlineedit


__version__ = "0.0.1"


class StuffListDialog(QDialog,
            ui_stufflistdialog_tabwidget.Ui_StuffListDialog) :
    
    WORK, WAIT = range(2)

    def __init__(self, stuffs=None, parent=None) :
        super(StuffListDialog, self).__init__(parent)
        self.setupUi(self)

        if stuffs is None :
            QMessageBox.warning(self,
                    "查看员工队列",
                    "当前列表中无此员工号.\n可以使用此工号.")
            return
        self.stuffs = stuffs 
        #print(self.stuffs)
        self.populateAllStuffTable()
        self.populateTable(self.WORK)
        self.populateTable(self.WAIT)
        self.buttonBox.button(QDialogButtonBox.Close).setText(
                                "退出")

    def keyPressEvent(self, event) :
        if event.key() == Qt.Key_Enter :
            event.ignore()
        elif event.key() == Qt.Key_Escape :
            QDialog.reject(self)
        else :
            QWidget.keyPressEvent(self, event)

    @pyqtSignature("int")
    def on_IdSpinBox_valueChanged(self, ID) :
        #print("ID: {}".format(ID))
        if (ID-1) <= self.allStuffTable.columnCount() :
            self.findTheStuff(self.allStuffTable, 0, ID-1)
            notFoundInAll = False
        else :
            notFoundInAll = True
        if (ID-1) <= self.workPosTable.columnCount() :
            self.findTheStuff(self.workPosTable, 0, ID-1)
            notFoundInWork = False
        else :
            notFoundInWork = True
        if (ID-1) <= self.waitPosTable.columnCount() :
            self.findTheStuff(self.waitPosTable, 0 ,ID-1)
            notFoundInWait = False
        else :
            notFoundInWait = True
        if notFoundInAll and notFoundInWork and notFoundInWait :
            QMessageBox.warning(self,
                    "员工工号错误",
                    "没有此工号."
                    "请查询后重新输入")

    def populateAllStuffTable(self) :
        IDs = self.stuffs.getIDs()
        print("IDs: {}".format(IDs))
        heads = [str(i) for i in IDs] 
        vHeads = ["员工工号", "姓名", "性别",
                        "工作次数", "等待位置", "工作位置"]
        self.allStuffTable.clear()
        self.allStuffTable.setSortingEnabled(False)
        self.allStuffTable.setRowCount(len(vHeads))
        self.allStuffTable.setColumnCount(len(IDs))
        self.allStuffTable.setVerticalHeaderLabels(vHeads)
        #for column, stuff in enumerate(self.stuffs) :
        for column, Id in enumerate(IDs) :
            print("Id: {}".format(Id))
            stuff = self.stuffs.stuffId(Id)
            item = QTableWidgetItem(str(stuff.Id))
            item.setData(Qt.UserRole, int(stuff.Id))
            self.allStuffTable.setItem(0, column, item)
            print("员工工号: {}".format(stuff.Id))
            self.allStuffTable.setItem(1, column,
                        QTableWidgetItem(str(stuff.name)))
            self.allStuffTable.setItem(2, column,
                        QTableWidgetItem(str(stuff.gender)))
            self.allStuffTable.setItem(3, column,
                        QTableWidgetItem(str(stuff.wTime)))
            #print("工作次数: {}".format(stuff.wTime))
            self.allStuffTable.setItem(4, column,
                        #QTableWidgetItem(str(stuff.waitPos)))
                        QTableWidgetItem(""
                        if stuff.waitPos is None else 
                            str(stuff.waitPos)))
            self.allStuffTable.setItem(5, column,
                        #QTableWidgetItem(str(stuff.workPos)))
                        QTableWidgetItem(""
                        if stuff.workPos is None else 
                            str(stuff.workPos)))
            item.setTextAlignment(Qt.AlignRight|Qt.AlignVCenter)
        self.allStuffTable.resizeColumnsToContents()
        #self.allStuffTable.setCurrentCell(0,0)
        #self.findTheStuff(self.allStuffTable, 0, 14)

    def on_allStuffTable_cellDoubleClicked(self, row, column) :
        print("行: {}, 列: {}".format(row, column))
        item = self.allStuffTable.item(0, column)
        if item is None :
            return None
        else :
            Id = int(item.data(Qt.UserRole))
        stuff = self.stuffs.stuffId(Id)
        if stuff is not None :
            form = updatestuffdialog_idlineedit.UpdateStuffDialog(
                                self.stuffs, stuff, self)
            if form.exec_() :
                self.populateAllStuffTable()
                self.populateTable(self.WORK)
                self.populateTable(self.WAIT)
        
    def on_workPosTable_cellDoubleClicked(self, row, column) :
        print("行: {}, 列: {}".format(row, column))
        item = self.workPosTable.item(row, column)
        if item is None :
            return None
        else :
            Id = int(item.data(Qt.UserRole))
        stuff = self.stuffs.stuffId(Id)
        if stuff is not None :
            form = updatestuffdialog_idlineedit.UpdateStuffDialog(
                                self.stuffs, stuff, self)
            if form.exec_() :
                self.populateAllStuffTable()
                self.populateTable(self.WORK)
                self.populateTable(self.WAIT)

    def on_waitPosTable_cellDoubleClicked(self, row, column) :
        print("行: {}, 列: {}".format(row, column))
        item = self.waitPosTable.item(row, column)
        if item is None :
            return None
        else :
            Id = int(item.data(Qt.UserRole))
        stuff = self.stuffs.stuffId(Id)
        if stuff is not None :
            form = updatestuffdialog_idlineedit.UpdateStuffDialog(
                                self.stuffs, stuff, self)
            if form.exec_() :
                self.populateAllStuffTable()
                self.populateTable(self.WORK)
                self.populateTable(self.WAIT)

    def whichTable(self, seq) :
        if seq is self.WORK :
            return self.workPosTable
        elif seq is self.WAIT :
            return self.waitPosTable
        else :
            print("错误序号,不做处理")

    def populateTable(self, seq) :
        workSeqs = self.stuffs.getWorkSeq()
        #print("员工队列: {}".format(workSeqs))
        maxWorkTime = self.stuffs.getMaxTime()
        #print("最大工作次数: {}".format(maxWorkTime))
        workTimes = range(( maxWorkTime + 1))
        if seq is self.WORK :
            lar = self.stuffs.getLargestWorkPos()
            #print("最大工作位置: {}".format(lar))
            headers = range(1,lar + 1)
        elif seq is self.WAIT :
            lar = self.stuffs.getLargestWaitPos()
            #print("最大等待位置: {}".format(lar))
            headers = range(1,lar + 1)
        headers = [ "序号:{}".format(header)
                        for header in headers ]
        self.whichTable(seq).clear()
        self.whichTable(seq).setSortingEnabled(False)
        self.whichTable(seq).setRowCount(maxWorkTime + 1)
        self.whichTable(seq).setColumnCount(len(headers))
        self.whichTable(seq).setHorizontalHeaderLabels(headers)
        self.whichTable(seq).setVerticalHeaderLabels(
            [ "工作次数: {}".format(i) for i in workTimes])
        for row, workSeq in enumerate(workSeqs) :
            for (workPos, Id) in workSeq.workPoses \
                    if seq is self.WORK else workSeq.waitPoses :
                print("员工位置: {}".format(workPos))
                item = QTableWidgetItem(str(workPos))
                item.setData(Qt.UserRole, int(Id))
                self.whichTable(seq).setItem(row,
                            (workPos - 1),
                            #(workPos),
                    item)
                item.setTextAlignment(
                        Qt.AlignRight|Qt.AlignVCenter)
        self.whichTable(seq).resizeColumnsToContents()

    def findTheStuff(self, table=None, row=0, column=0) :
        if table is not None :
            table.setCurrentCell(row,column)

    def populateWorkPosTable(self) :
        workSeqs = self.stuffs.getWorkSeq()
        #print(workSeqs)
        maxWorkTime = self.stuffs.getMaxTime()
        #print(maxWorkTime)
        workTimes = range(( maxWorkTime + 1))
        headers = range(1,self.stuffs.getLargestId() + 1)
        headers = [ "序号:{}".format(header)
                        for header in headers ]
        self.workPosTable.clear()
        self.workPosTable.setSortingEnabled(False)
        self.workPosTable.setRowCount(maxWorkTime + 1)
        self.workPosTable.setColumnCount(len(headers))
        self.workPosTable.setHorizontalHeaderLabels(headers)
        self.workPosTable.setVerticalHeaderLabels(
            [ "工作次数: {}".format(i) for i in workTimes])
        for row, workSeq in enumerate(workSeqs) :
            for workPos in workSeq.workPoses :
                #print(workPos)
                self.workPosTable.setItem(row,
                            (workPos - 1),
                            QTableWidgetItem(str(workPos)))
        self.workPosTable.resizeColumnsToContents()

if __name__ == '__main__' :
    import sys

    S = stuffdata.StuffContainer()
    S.addStuffs(S.MALE, 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15)
    S.stuffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12,13,14,15)
    S.stuffsWork(S.NOR,1, 2, 3, 4, 6, 8, 9)
    #S.stuffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)

    app = QApplication(sys.argv)
    form = StuffListDialog(S)
    form.show()
    sys.exit(app.exec_())
