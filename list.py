#-*- coding:utf-8 -*-
'''
TableWidget
'''
__author__ = 'Tony Zhu'
import sys, os
import time
import _thread

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.QtCore import  Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel,  QTableWidget,QHBoxLayout, QTableWidgetItem, QComboBox,QFrame,QDesktopWidget
from PyQt5.QtGui import QFont,QColor,QBrush,QPixmap
from PyQt5.QtCore import QTimer

#from cansend import Ectrl
from ehub import EHub

sendcnt = [0, 0]
CanSendId = ["", ""]
CanSendStr = ["", ""]


#send_tuple = ("发送报文", "发送", ["", "", ""])




recvcnt = [0,0,0,0]
CanRecvId = ["", "", "", ""]
CanRecvStr = ["", "", "", ""]
FCW_str = ''
HW_str = ''


VideoPlaying = 0
VideoPlayStart = 1
FPGATestResult = 0

def play_video():
    os.system("python3 cv_play_video.py")

class PlayThread(QThread):
    trigger = pyqtSignal()
    def __init__(self):
        super(PlayThread,self).__init__()

    def run(self):
        global FPGATestResult
        global VideoPlaying
        global VideoPlayStart

        print ("play start")
        VideoPlaying = 1
        play_video()
        VideoPlaying = 0
        VideoPlayStart = 0

        if FPGATestResult != 2:
            FPGATestResult = 3
        self.trigger.emit()         #循环完毕后发出信号

class TableSheet(QWidget):
    def __init__(self):
        super().__init__()

        self.Rline = 7
        self.CntLine = 6
        self.TestOKCnt = 0
        self.TestErrcnt = 0
        self.timer = None
        self.display_flag = 1
        self.test_flag = 0
        self.PlayButton = None
        self.DisplayButton = None
        self.TestButton = None

        self.workThread=WorkThread()
        #self.workThread.trigger.connect(table.update_recv_buf)
        #self.workThread.start()              #计时开始

        self.playThread=PlayThread()
        self.playThread.trigger.connect(self.video_play_over)

        self.create_table()

    def create_table(self):
        self.CreateTableHeader()
        self.TableAddOneLine(0, "车速报文", "发送", "", "0", "")
        self.TableAddOneLine(1, "控制报文", "发送", "", "0", "")
        self.TableAddOneLine(2, "识别报文", "接收", "", "0", "")
        self.TableAddOneLine(3, "识别报文", "接收", "", "0", "")
        self.TableAddOneLine(4, "报警报文", "接收", "", "0", "")
        self.TableAddOneLine(5, "系统报文", "接收", "", "0", "")
        self.TableSetOneLine(self.CntLine, "总计数", "", "未通过", "", "")
        self.TableAddResultLine(self.Rline, "", "")
        self.TableLayOut()

    def CreateTableHeader(self):
        horizontalHeader = ["报文种类","方向","ID","幀计数","内容"]
        #self.setWindowTitle('TableWidget Usage')
        self.setWindowTitle('CAN 报文信息')
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(8)

        self.table.setHorizontalHeaderLabels(horizontalHeader)
        #self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setEditTriggers(QTableWidget.CurrentChanged)
        #self.table.setSelectionBehavior(QTableWidget.SelectColumns)
        self.table.setSelectionBehavior(QTableWidget.SelectItems)
        self.table.setSelectionMode(QTableWidget.SingleSelection  )

        for index in range(self.table.columnCount()):
            headItem = self.table.horizontalHeaderItem(index)
            #字体
            #headItem.setFont(QFont("song", 12, QFont.Bold))
            headItem.setFont(QFont("song", 12, QFont.Bold))
            headItem.setForeground(QBrush(Qt.gray))
            headItem.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

    def TableLayOut(self):
        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.table)
        self.setLayout(mainLayout)
        #设置UI的距离和宽、高
        #self.setGeometry(300, 300, 740, 200)
        self.setGeometry(300, 300, 800, 450)
        self.button_init()
        self.center()

    def button_init(self):
        self.PlayButton = self.create_button("播放", "play", 25, 400, self.pre_play_video)
        self.DisplayButton = self.create_button("暂停显示", "display", 600, 400, self.display_switch)
        self.TestButton = self.create_button("开始测试", "test", 300, 400, self.test_switch)
        self.TestButton = self.create_button("输入序列号", "input", 250, 400, self.get_serialnum)

    def create_button(self, name, tips, x, y, func):
        Button = QPushButton(self)
        Button.setText(name)          #text
        #self.Button.setIcon(QIcon("close.png")) #icon
        #self.Button.setShortcut('Ctrl+D')  #shortcut key
        #self.Button.clicked.connect(self.close)
        #self.Button.clicked.connect(self.playThread.start)
        Button.clicked.connect(func)
        Button.setToolTip(tips) #Tool tip
        Button.move(x, y)
        return Button

    def SetItemFont(self, str1):
        newItem = QTableWidgetItem(str1)
        #textFont = QFont("song", 18, QFont.Bold)
        textFont = QFont("song", 18)
        newItem.setFont(textFont)

        return newItem


    def TableSetOneLine(self, line, str1, str2, str3, str4, str5):

        self.table.setColumnWidth(4,300)
        self.table.setRowHeight(line,40)

        self.table.setItem(line, 0, QTableWidgetItem(str1))
        self.table.setItem(line, 1, QTableWidgetItem(str2))
        self.table.setItem(line, 2, QTableWidgetItem(str3))
        self.table.setItem(line, 3, QTableWidgetItem(str4))
        self.table.setItem(line, 4, QTableWidgetItem(str5))

    def TableAddResultLine(self,line, str1, str2):

        #设置列宽
        self.table.setColumnWidth(4,300)
        #设置行高
        self.table.setRowHeight(line,60)
        #self.table.setFrameShape(QFrame.HLine)#设定样式
        #self.table.setShowGrid(False) #取消网格线
        #self.table.verticalHeader().setVisible(False) #隐藏垂直表头

        self.table.setItem(line, 0, self.SetItemFont("HW"))
        self.table.setItem(line, 1, self.SetItemFont(str1))
        self.table.setItem(line, 2, self.SetItemFont("FCW"))
        self.table.setItem(line, 3, self.SetItemFont(str2))

        newItem = QTableWidgetItem("等待测试 ...")
        #textFont = QFont("song", 18, QFont.Bold)
        textFont = QFont("song", 18)
        newItem.setFont(textFont)
        #newItem.setFlags(newItem.flags() | Qt.ItemIsEditable)
        #newItem.setFlags(newItem.flags() & ~Qt.ItemIsEditable)

        #newItem.setForeground(QBrush(Qt.green))
        #newItem.setBackground(QBrush(Qt.gray))
        #newItem.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        newItem.setTextAlignment(Qt.AlignVCenter)
        self.table.setItem(line,4,newItem)

    def SetResultDsip(self, row, clomuns, str1, clor):
        newItem = QTableWidgetItem(str1)
        newItem.setForeground(QBrush(clor))
        self.table.setItem(row, clomuns, newItem)

    #def SetResultDsip(self, row, clomuns, str1, font = "song", fontsize=18):
    #    newItem = QTableWidgetItem(str1)
    #    #newItem.setBackground(QBrush(Qt.gray))
    #    textFont = QFont(font, fontsize)
    #    newItem.setFont(textFont)
    #    self.table.setItem(row, clomuns, newItem)

    def SetResultWait(self, line, n, str1):
        newItem = QTableWidgetItem(str1)
        newItem.setBackground(QBrush(Qt.gray))
        textFont = QFont("song", 18)
        newItem.setFont(textFont)
        self.table.setItem(line, n, newItem)
    def SetResultPass(self, line, n):
        newItem = QTableWidgetItem("测试通过")
        textFont = QFont("song", 18)
        newItem.setFont(textFont)
        newItem.setForeground(QBrush(Qt.green))
        newItem.setBackground(QBrush(Qt.gray))
        self.table.setItem(line, n, newItem)
    def SetResultFail(self, line, n):
        newItem = QTableWidgetItem("测试失败")
        textFont = QFont("song", 18)
        newItem.setFont(textFont)
        newItem.setForeground(QBrush(Qt.red))
        newItem.setBackground(QBrush(Qt.gray))
        self.table.setItem(line, n, newItem)
    def SetWarnResult(self,line, n, str1):
        newItem = QTableWidgetItem(str1)
        textFont = QFont("song", 18)
        newItem.setFont(textFont)
        newItem.setForeground(QBrush(Qt.red))
        #newItem.setBackground(QBrush(Qt.gray))
        self.table.setItem(line, n, newItem)

    def TableAddOneLine(self, line, device, direction, canid, pkgcnt, buf):

        #设置列宽
        self.table.setColumnWidth(4,300)
        #设置行高
        self.table.setRowHeight(line,40)
        #self.table.setFrameShape(QFrame.HLine)#设定样式
        #self.table.setShowGrid(False) #取消网格线
        #self.table.verticalHeader().setVisible(False) #隐藏垂直表头

        self.table.setItem(line, 0, QTableWidgetItem(device))

        genderComb = QComboBox()
        genderComb.addItem(direction)
        genderComb.setCurrentIndex(0)
        self.table.setCellWidget(line, 1, genderComb)

        self.table.setItem(line,2,QTableWidgetItem(canid))
        self.table.setItem(line,3,QTableWidgetItem(pkgcnt))
        self.table.setItem(line,4,QTableWidgetItem(buf))

    #控制窗口显示在屏幕中心的方法
    def center(self):
        #获得窗口
        qr = self.frameGeometry()
        #获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        #显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def get_serialnum(self):
        #print (unicode(self.table.item(6,1)))
        str1 = self.table.item(6,4).text()

        #print(bytes(str1, encoding='gbk'))
        #print(str(str1, encoding='utf-8'))
        #print(str(str1, encoding='unicode'))
        print(str1)


        #print ((str)(str1))
        #print (str1.back())
        pass

    def test_switch(self):
        button_name = ('开始测试', '停止测试')
        self.test_flag ^= 1
        self.TestButton.setText(button_name[self.test_flag])          #text

        if self.test_flag:
            self.workThread.timer_start()
            self.display_timer_start()
            self.pre_play_video()
        else:
            self.workThread.timer_stop()
            self.display_timer_stop()

    def video_play_over(self):
        global FPGATestResult
        self.test_switch()

        #self.test_stop()
        FPGATestResult = 0
        print (FPGATestResult)

    def test_stop(self):
        button_name = ('开始测试', '停止测试')
        self.workThread.timer_stop()
        self.display_timer_stop()
        self.TestButton.setText(button_name[0])          #text

    def display_switch(self):
        button_name = ('继续显示', '暂停显示')
        #button_name = ('a', 'b')
        self.display_flag ^= 1
        self.DisplayButton.setText(button_name[self.display_flag])          #text

    def auto_play_video(self):
        if VideoPlayStart == 1:
            self.pre_play_video()

    def pre_play_video(self):
        global FPGATestResult
        if VideoPlaying == 0:
            FPGATestResult = 1
            self.playThread.start()
        else:
            print ("video playing")
    def update_send_buf(self):
        for i in range(len(sendcnt)):
            self.table.setItem(0+i, 2, QTableWidgetItem(CanSendId[i]))
            self.table.setItem(0+i, 3, QTableWidgetItem(str(sendcnt[i])))
            self.table.setItem(0+i, 4, QTableWidgetItem(CanSendStr[i]))
    def update_recv_buf(self):
        for i in range(len(recvcnt)):
            self.table.setItem(2+i, 2, QTableWidgetItem(CanRecvId[i]))
            self.table.setItem(2+i, 3, QTableWidgetItem(str(recvcnt[i])))
            self.table.setItem(2+i, 4, QTableWidgetItem(CanRecvStr[i]))
    def update_warning(self):
        print ("update warning %d" % FPGATestResult)
        #self.auto_play_video()
        self.SetWarnResult(self.Rline, 1, FCW_str)
        self.SetWarnResult(self.Rline, 3, HW_str)

        if FPGATestResult == 0:
            self.SetResultWait(self.Rline, 4, "等待测试 ...")
        elif FPGATestResult == 1:
            self.SetResultWait(self.Rline, 4, "测试中 ...")
        elif FPGATestResult == 2:
            self.SetResultPass(self.Rline, 4)
            self.TestOKCnt += 1
            self.SetResultDsip(self.CntLine, 1, str(self.TestOKCnt), Qt.black)
        elif FPGATestResult == 3:
            self.SetResultFail(self.Rline, 4)
            self.TestErrcnt += 1
            self.SetResultDsip(self.CntLine, 3, str(self.TestErrcnt), Qt.red)

    def display_timer_start(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.operate)
        self.timer.start(20)
    def display_timer_stop(self):
        self.operate()
        self.timer.stop()

    def operate(self):
        if self.display_flag:
            self.update_send_buf()
            self.update_recv_buf()
            self.update_warning()
            #print ("update")

class Candata():

    def __init__(self):
        self.ehub = EHub()
        print ("candata enter")

    def send_can_msg(self):
        global sendcnt
        global CanSendId
        global CanSendStr
        #print ("send")

        CanID = [0x18FEF100, 0x0CFDCC27]
        data = [[0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8], [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8]]

        speed = 60*256
        data[0][1] = speed & 0xFF
        data[0][2] = (speed >> 8) & 0xFF

        data[1][6] &= ~0x04 #left disable
        data[1][6] &= ~0x08 #right diable

        for index in range(2):
            CanSendId[index] = ("0x%X" % (CanID[index]))
            CanSendStr[index] = ''
            for i in range(len(data[index])):
                CanSendStr[index] += ("0x%02X, " % ( data[index][i]))
            self.ehub.send_can_frame(CanID[index], data[index])
            sendcnt[index] += 1

    def recv_can_msg(self):
        global recvcnt
        global CanRecvStr
        global CanRecvId
        global HW_str, FCW_str, FPGATestResult
        global VideoPlayStart
        index = 0
        #print ("recv")
        datalen, recvbuf = self.ehub.recv_can_frame()
        #std_id, ext_id, data = self.ehub.recv_can_frame()
        #print (" id = 0x%X" % ext_id)

        print ("recv can data len = %d" % (datalen))
        pkgcnt = datalen//20
        step = 0;
        for j in range(pkgcnt):
            #print ("step = %d" % (step))
            std_id, ext_id, data = self.ehub.get_can_frame(recvbuf[step:step+20])
            step += 20
            print ("std_id = 0x%X, ext_id = 0x%X" % (std_id, ext_id))
            #for i in range(len(data)):
            #    print ("0x%02X, " % ( data[i]))

            #print (data)
            if std_id == 0 and ext_id == 0:
                return

            if ext_id == 0x10FE6FE8:
                index = 0
            if ext_id == 0x18FE5BE8:
                index = 1
            if ext_id == 0x10F007E8:
                index = 2
                fcw_stat = data[1][0] & 0x01
                hw_focus = data[2][0] & 0x01

                if fcw_stat == 1:
                    print ("FCW...");
                    FCW_str = "告警"
                    if fcw_stat == 1:
                        FPGATestResult = 2
                else:
                    FCW_str = ""

                if hw_focus == 1:
                    print ("HW...");
                    HW_str = "告警"
                else:
                    HW_str = ""

            if ext_id == 0x18FECAE8:
                index = 3

            CanRecvId[index] = ("0x%X" % (ext_id))
            recvcnt[index] += 1
            CanRecvStr[index] = ''
            for i in range(len(data)):
                CanRecvStr[index] += ("0x%02X, " % ( data[i]))

        #if recvcnt[0] > 5:
        #    #VideoPlayStart = 1
        #    pass

class WorkThread(QThread):
    trigger = pyqtSignal()
    can = Candata()
    def __init__(self):
        super(WorkThread,self).__init__()
    def run(self):
        while 1:
            self.can.recv_can_msg()
            #self.trigger.emit()         #循环完毕后发出信号

    def timer_start(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.operate)
        self.timer.start(1000)
    def timer_stop(self):
        self.timer.stop()

    def operate(self):
        self.can.send_can_msg()
        self.can.recv_can_msg()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    table = TableSheet()


    table.show()
    sys.exit(app.exec_())

