#!/usr/bin/python3
# File Info : 
#   The UpdateStuffDialog class defined in this file.

from PyQt4.QtCore import *
from PyQt4.QtGui import *
#import stuffdata
import ui_updatestuffdialog_idlineedit


__version__="0.2.0"


class UpdateStuffDialog(QDialog,
        ui_updatestuffdialog_idlineedit.Ui_UpdateStuffDialog) :

    def __init__(self, stuffs, stuff=None, parent=None) :
        super(UpdateStuffDialog, self).__init__(parent)
        self.setupUi(self)

        self.stuffs = stuffs
        self.stuff = stuff
        self.unavaliableIDs = []
        if stuff is not None :
            Id = stuff.Id
            self.IdLineEdit.setText("{}".format(Id))
            self.IdLineEdit.setReadOnly(True)
            self.nameLineEdit.setText(stuff.name)
            self.genderComboBox.setCurrentIndex(
                self.genderComboBox.findText(stuff.gender))
            self.wTimeSpinBox.setEnabled(True)
            self.wTimeSpinBox.setValue(stuff.wTime)
            self.wTypeComboBox.setEnabled(True)
            self.wTypeComboBox.setCurrentIndex(
                self.wTypeComboBox.findText(stuff.wType))
            if stuff.wType is self.stuffs.WAIT :
                #self.wTimeSpinBox.setEnabled(True)
                self.waitPosSpinBox.setEnabled(True)
                self.waitPosSpinBox.setValue(stuff.waitPos)
            elif stuff.wType is (self.stuffs.NOR or
                    self.stuffs.SEL or self.stuffs.NAMED) :
                #self.wTimeSpinBox.setEnabled(True)
                self.workPosSpinBox.setEnabled(True)
                self.workPosSpinBox.setValue(stuff.workPos)
            #elif stuff.wType is self.stuffs.IDLE :
            else :
                print("员工工作类型: {}".format(stuff.wType))
                self.wTimeSpinBox.setEnabled(False)
            self.buttonBox.button(QDialogButtonBox.Ok).setText(
                                    "确认修改(&A)")
            self.buttonBox.button(QDialogButtonBox.Cancel).setText(
                                    "放弃修改")
            self.setWindowTitle("编辑员工信息")
            self.nameLineEdit.setFocus()
        else :
            self.IdLineEdit.setFocus()

    @pyqtSignature("int")
    def on_wTypeComboBox_activated(self, index) :
        self.updateDialog(index=index)

    def accept(self) :
        print("点击了确定键")
        name = self.nameLineEdit.text()
        gender = self.getGender()
        if self.stuff is None :
            print("添加模式")
            IDs = [ int(i) for i
                in self.IdLineEdit.text().split() ]
            #for Id in self.IdLineEdit.text().split() :
                #print("工号为: {}".format(Id))
                #Id = int(Id)
            if self.checkAndWarn(Id=IDs) :
                print("已有员工工号,提示!")
                QMessageBox.warning(self,
                        "员工工号错误",
                        "请查询后重新输入"
                        "已有工号:\n"
                        "{}".format(self.unavaliableIDs))
                self.IdLineEdit.clear()
                self.unavaliableIDs = []
                return
            else :
                for Id in IDs :
                    print("没有该工号")
                    self.stuffs.updateStuff(Id)
                    print("新建成功!")
                    self.stuffs.tell(Id)
            QMessageBox.information(self,
                "操作成功!",
                "员工添加成功!\t\n"
                "工号: {}".format(self.IdLineEdit.text()))
        else :
            Id = self.stuff.Id
            name = self.nameLineEdit.text()
            wTime = self.wTimeSpinBox.value()
            if self.checkAndWarn(wTime=wTime) :
                #self.stuffs.setWorkTime(Id, wTime)
                self.stuffs.updateWorkStatus(Id=Id, wTime=wTime)
            wType = self.getWorkType()
            if wType is (self.stuffs.NOR or
                    self.stuffs.NAMED or self.stuffs.SEL) :
                workPos = self.workPosSpinBox.value()
                if not self.checkAndWarn(wTime=wTime,
                            workPos=workPos) :
                    return
                #self.stuffs.setWorkPos(Id, workPos)
                #self.stuffs.setWorkType(Id, wType)
                self.stuffs.updateWorkStatus(Id=Id, workPos=workPos,
                                                    wType=wType)
            elif wType is self.stuffs.WAIT :
                waitPos = self.waitPosSpinBox.value()
                if not self.checkAndWarn(wTime=wTime,
                            waitPos=waitPos) :
                    return
                #self.stuffs.setWaitPos(Id, waitPos)
                #self.stuffs.setWorkType(Id, wType)
                self.stuffs.updateWorkStatus(Id=Id, waitPos=waitPos,
                                                    wType=wType)
            QMessageBox.information(self,
                "操作成功!",
                "成功修改员工信息!\t\n"
                "工号: {}".format(Id))
        self.stuffs.updateStuff(Id=Id,gender=gender,
                            name=name)
        self.stuffs.tell(Id)
        QDialog.accept(self)


    def updateDialog(self, index=None, text=None) :
        if index is not None :
            print("index: {}".format(index))
            if index is (0 or 1 or 2) :
                print("index = 0 1 2")
                self.wTimeSpinBox.setEnabled(True)
                self.workPosSpinBox.setEnabled(True)
                self.waitPosSpinBox.setEnabled(False)
            elif index is 3 :
                print("index = 3")
                self.wTimeSpinBox.setEnabled(True)
                self.workPosSpinBox.setEnabled(False)
                self.waitPosSpinBox.setEnabled(True)
            elif index is 4 :
                print("index = 4")
                self.wTimeSpinBox.setEnabled(False)
                self.workPosSpinBox.setEnabled(False)
                self.waitPosSpinBox.setEnabled(False)
            else :
                print("index: {}".format(index))
                print("Nothing happend.\nunknown erreo.")
            

    def checkAndWarn(self, Id=None, wTime=0,
            waitPos=None, workPos=None) :
        maxTime = self.stuffs.getMaxTime()
        print("当前工作队列最大次数: {}".format(maxTime))
        if wTime > maxTime :
            print("当前输入工作次数超出工作队列最大次数")
            reply = QMessageBox.question(self,
                    "提示",
                    "没有当前输入工作次数对应的工作队列."
                    "\n是否需要自动创建?",
                    QMessageBox.Yes|QMessageBox.No)
            if reply == QMessageBox.Yes :
                print("调用updateMaxSeqByTime()")
                self.stuffs.updateMaxSeqByTime(wTime)
            else :
                return False
        if Id is not None :
            for ID in Id :
                print("Check Stuff Id")
                if self.stuffs.stuffId(ID) :
                    self.unavaliableIDs.append(ID)
                else :
                    pass
            return self.unavaliableIDs
        print("wTime: {}".format(wTime))
        if waitPos is not None :
            print("Check waitPos: {}".format(waitPos))
            if not self.stuffs.waitPosAvaliable(wTime,
                                    waitPos) :
                QMessageBox.warning(self,
                        "员工等待位置错误",
                        "此等待位置已有员工.\t\n"
                        "请查询后重新输入")
                return False
        if workPos is not None :
            print("Check workPos: {}".format(workPos))
            if not self.stuffs.workPosAvaliable(wTime,
                                    workPos) :
                print("已有员工工号")
                QMessageBox.warning(self,
                        "员工工作位置错误",
                        "此工作位置已有员工.\t\n"
                        "请查询后重新输入")
                return False
        return True

    def getWorkType(self) :
        if self.wTypeComboBox.currentIndex() is 0 :
            return self.stuffs.NOR
        elif self.wTypeComboBox.currentIndex() is 1 :
            return self.stuffs.NAMED
        elif self.wTypeComboBox.currentIndex() is 2 :
            return self.stuffs.SEL
        elif self.wTypeComboBox.currentIndex() is 3 :
            return self.stuffs.WAIT
        elif self.wTypeComboBox.currentIndex() is 4 :
            return self.stuffs.IDLE

    def getGender(self) :
        if self.genderComboBox.currentIndex() is 0 :
            return self.stuffs.MALE
        elif self.genderComboBox.currentIndex() is 1 :
            return self.stuffs.FEMALE

if __name__ == "__main__":
    import sys

    S = stuffdata.StuffContainer()
    S.addStuffs(S.MALE, 1,2,3,4,5,6,7,8,9)
    S.stuffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    S.stuffsWork(S.NOR,1, 2, 3, 4, 5, 6, 7, 8, 9)

    app = QApplication(sys.argv)
    form = UpdateStuffDialog(S, S.stuffId(8))
    #form = UpdateStuffDialog(S)
    form.show()
    sys.exit(app.exec_())

