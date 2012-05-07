#!/usr/bin/python3
# File Info : 
#   The UpdateStaffDialog class defined in this file.

# PyQt #
from PyQt4.QtCore import *
from PyQt4.QtGui import *

# 引用#
import staffdata

# 正则 #
import re


class UpdateStaffDialog(QDialog) :


    #{{{ # 初始化更新员工信息窗口 #
    def __init__(self, staffs, staff=None, parent=None) :
        super(UpdateStaffDialog, self).__init__(parent)
        self.staff = staff
        self.staffs = staffs
        self.setupUi()

        self.workSeqs = staffs.getWorkSeq()
        self.unavaliableIDs = []
        if staff is not None :
            # 1. 获得员工信息
            Id = staff.Id
            name = staff.name
            gender = staff.gender
            wTime = staff.wTime
            wType = staff.wType
            group = staff.group
            if wType == self.staffs.IDLE :
                pos = None
            else :
                nSeq = self.workSeqs[wTime].nSeq
                pos = nSeq.index(staff)
            # 2. 设置显示文字
            self.IdLineEdit.setText("{}".format(Id))
            self.IdLineEdit.setReadOnly(True)
            self.nameLineEdit.setText(name)
            self.genderComboBox.setCurrentIndex(
                self.genderComboBox.findText(gender))
            if group is not None :
                self.groupNumLabel.setText("\t{}".format(group))
            self.wTimeLabel.setText("工作次数: {}".format(wTime))
            self.wTypeLabel.setText("工作类型: {}".format(wType))
            if wType is self.staffs.WAIT :
                self.posLabel.setText("等待位置: {}".format(pos))
            elif staff.wType in staffs.workTypes :
                self.posLabel.setText("{}位置: {}".format(wType, pos))
            else :
                self.posLabel.setText("")
            self.buttonBox.button(QDialogButtonBox.Ok).setText(
                                    "确认修改(&A)")
            self.buttonBox.button(QDialogButtonBox.Cancel).setText(
                                    "放弃修改")
            self.setWindowTitle("编辑员工信息")
            self.nameLineEdit.setFocus()
        else :
            self.IdLineEdit.setFocus()
            self.posLabel.setText("")
            self.wTimeLabel.setText("工作次数: ")
            self.wTypeLabel.setText("工作类型:")

        # 链接信号 #
        self.connect(self.buttonBox, SIGNAL("accepted()"),
                        self.accept)
        self.connect(self.buttonBox, SIGNAL("rejected()"),
                        self.reject)
    #}}}

    #{{{ # 设置界面 #
    def setupUi(self) :
        #-- 添加组件 --#

        # 标签 #
        infoLabel = QLabel("员工信息:", self)
        IdLabel = QLabel("工号:", self)
        nameLabel = QLabel("姓名:", self)
        genderLabel = QLabel("性别:", self)
        groupLabel = QLabel("员工分组:", self)
        groupNumLabel = QLabel("", self)
        workStatusLabel = QLabel("员工工作状态:", self)
        wTimeLabel = QLabel("工作次数:", self)
        wTypeLabel = QLabel("工作类型:", self)
        posLabel = QLabel("位置:", self)
        # 挂入对话框 #
        self.groupNumLabel = groupNumLabel 
        self.wTimeLabel = wTimeLabel
        self.wTypeLabel = wTypeLabel
        self.posLabel = posLabel

        # 编辑框 #
        self.IdLineEdit = QLineEdit(self)
        self.IdLineEdit.setAlignment(Qt.AlignRight)
        self.nameLineEdit = QLineEdit(self)
        self.nameLineEdit.setAlignment(Qt.AlignRight)

        # 选项框 #
        genderComboBox = QComboBox(self)
        genderComboBox.addItem("男")
        genderComboBox.addItem("女")
        # 挂入对话框 #
        self.genderComboBox = genderComboBox

        # 分割线 #
        Hline = QFrame(self)
        Hline.setFrameShape(QFrame.HLine)
        Hline.setFrameShadow(QFrame.Sunken)
        Vline = QFrame(self)
        Vline.setFrameShape(QFrame.VLine)
        Vline.setFrameShadow(QFrame.Sunken)

        # 按键组 #
        buttonBox = QDialogButtonBox(self)
        buttonBox.setOrientation(Qt.Vertical)
        buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        buttonBox.button(QDialogButtonBox.Ok).setText("确认添加")
        buttonBox.button(QDialogButtonBox.Cancel).setText("放弃添加")
        # 挂入对话框 #
        self.buttonBox = buttonBox

        #-- 组织结构 --#

        # 左上(格子) #
        gridLayout = QGridLayout()
        gridLayout.setColumnStretch(0, 2)
        gridLayout.setColumnStretch(1, 1)
        GaddWidget = gridLayout.addWidget
        GaddWidget(infoLabel, 0, 0, 1, 1)
        GaddWidget(IdLabel, 1, 0, 1, 1)
        GaddWidget(self.IdLineEdit, 1, 1, 1, 1)
        GaddWidget(nameLabel, 2, 0, 1, 1)
        GaddWidget(self.nameLineEdit, 2, 1, 1, 1)
        GaddWidget(genderLabel, 3, 0, 1, 1)
        GaddWidget(genderComboBox, 3, 1, 1, 1)
        GaddWidget(groupLabel, 4, 0, 1, 1)
        GaddWidget(groupNumLabel, 4, 1, 1, 1)

        # 左(纵) #
        VBoxLayout = QVBoxLayout()
        VaddWidget = VBoxLayout.addWidget
        VBoxLayout.addLayout(gridLayout)
        VaddWidget(Hline)
        VaddWidget(workStatusLabel)
        VaddWidget(self.wTimeLabel)
        VaddWidget(self.wTypeLabel)
        VaddWidget(self.posLabel)

        
        # 对话框结构 #
        HBoxLayout = QHBoxLayout()
        HBoxLayout.addLayout(VBoxLayout)
        HBoxLayout.addWidget(Vline)
        HBoxLayout.addWidget(buttonBox)

        # 对话框属性 # 
        self.setLayout(HBoxLayout)
        self.resize(326, 328)
        self.setMinimumSize(QSize(326, 328))
    #}}}
    
    #{{{ # 重定义: 确定键 #
    def accept(self) :
        updateStaff = self.staffs.updateStaff
        name = self.nameLineEdit.text()
        gender = self.getGender()
        if self.staff is None :
            p = re.compile(r'\D+')
            rawdata = self.IdLineEdit.text()
            data = re.split(p, rawdata)
            IDs = [ int(i) for i in  data if i.isdigit() ]
            if self.checkAndWarn(IDs=IDs) :
                QMessageBox.warning(self,
                        "员工工号错误",
                        "请查询后重新输入"
                        "已有工号:\n"
                        "{}".format(self.unavaliableIDs))
                self.unavaliableIDs = []
                return
            else :
                for Id in IDs :
                    updateStaff(Id, gender, name)
            QMessageBox.information(self,
                "操作成功!",
                "员工添加成功!\t\n"
                "工号: {}\n姓名: {}\n性别: {}"\
                    .format(IDs,
                        self.nameLineEdit.text(),
                        self.genderComboBox.currentText()))
        else :
            Id = self.staff.Id
            name = self.nameLineEdit.text()
            QMessageBox.information(self,
                "操作成功!",
                "成功修改员工信息!\t\n"
                "工号: {}".format(Id))
            updateStaff(Id=Id,gender=gender,
                                name=name)
        QDialog.accept(self)
    #}}}


    #{{{ #---- 辅助函数 ----#

    # 检查 Id 有效性 #

    def checkAndWarn(self, IDs=None) :
        if IDs is not None :
            for Id in IDs :
                if self.staffs.getStaff(Id) :
                    self.unavaliableIDs.append(Id)
            return self.unavaliableIDs

    # 取得员工性别 #

    def getGender(self) :
        if self.genderComboBox.currentIndex() is 0 :
            return self.staffs.MALE
        elif self.genderComboBox.currentIndex() is 1 :
            return self.staffs.FEMALE
    #}}}

if __name__ == "__main__":
    import sys

    S = staffdata.StaffContainer()
    S.addStaffs(S.MALE, 1,2,3,4,5,6,7,8,9)
    S.groupStaff(3,3)
    S.staffsWait(1, 2, 3, 4, 5, 6, 7, 8, 9)
    S.staffsWork(S.NOR, 4, 5, 6, 7, 8, 9)
    S.staffsWork(S.SEL, 1,2)
    S.staffsWork(S.NAMED, 3)

    app = QApplication(sys.argv)
    #form = UpdateStaffDialog(S, S.getStaff(3))
    form = UpdateStaffDialog(S)
    form.show()
    sys.exit(app.exec_())

