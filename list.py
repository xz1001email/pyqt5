#-*- coding:utf-8 -*-
'''
TableWidget
'''
__author__ = 'Tony Zhu'
import sys
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

CanSendStr = ''
CanRecvStr = ''
CanRecvId = ''
CanSendId = ''
sendcnt = 0
recvcnt = 0
class TableSheet(QWidget):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.count_start()

    def initUi(self):
        horizontalHeader = ["设备","ID","方向","幀计数","内容"]
        #self.setWindowTitle('TableWidget Usage')
        self.setWindowTitle('CAN 报文信息')
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(2)

        self.table.setHorizontalHeaderLabels(horizontalHeader)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectColumns)
        self.table.setSelectionMode(QTableWidget.SingleSelection  )

        for index in range(self.table.columnCount()):
            headItem = self.table.horizontalHeaderItem(index)
            #字体
            #headItem.setFont(QFont("song", 12, QFont.Bold))
            headItem.setFont(QFont("song", 12, QFont.Bold))
            headItem.setForeground(QBrush(Qt.gray))
            headItem.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        #设置列宽
        self.table.setColumnWidth(4,300)
        #设置行高
        self.table.setRowHeight(0,40)
        self.table.setRowHeight(1,40)
        #self.table.setFrameShape(QFrame.HLine)#设定样式
        #self.table.setShowGrid(False) #取消网格线
        #self.table.verticalHeader().setVisible(False) #隐藏垂直表头

        #设置第一行
        self.table.setItem(0,0, QTableWidgetItem("CAN0"))
        self.table.setItem(0,1,QTableWidgetItem("0"))
        genderComb = QComboBox()
        genderComb.addItem("发送")
        #genderComb.addItem("接收")
        genderComb.setCurrentIndex(0)
        self.table.setCellWidget(0,2,genderComb)
        self.table.setItem(0,3,QTableWidgetItem("0"))
        self.table.setItem(0,4,QTableWidgetItem("can send frame"))

        #设置第二行
        self.table.setItem(1,0, QTableWidgetItem("CAN0"))
        self.table.setItem(1,1,QTableWidgetItem("0"))
        genderComb = QComboBox()
        #genderComb.addItem("发送")
        genderComb.addItem("接收")
        genderComb.setCurrentIndex(0)
        #genderComb.setCurrentIndex(1)
        self.table.setCellWidget(1,2,genderComb)
        self.table.setItem(1,3,QTableWidgetItem("0"))
        self.table.setItem(1,4,QTableWidgetItem("can recv frame"))

        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.table)
        self.setLayout(mainLayout)
        #设置UI的距离和宽、高
        self.setGeometry(300, 300, 740, 200)
        self.center()

    #控制窗口显示在屏幕中心的方法
    def center(self):
        #获得窗口
        qr = self.frameGeometry()
        #获得屏幕中心点
        cp = QDesktopWidget().availableGeometry().center()
        #显示到屏幕中心
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def update_send_buf(self):
        self.table.setItem(0,1,QTableWidgetItem(CanSendId))
        self.table.setItem(0,3,QTableWidgetItem(str(sendcnt)))
        self.table.setItem(0,4,QTableWidgetItem(CanSendStr))
    def update_recv_buf(self):
        self.table.setItem(1,1,QTableWidgetItem(CanRecvId))
        self.table.setItem(1,3,QTableWidgetItem(str(recvcnt)))
        self.table.setItem(1,4,QTableWidgetItem(CanRecvStr))

    def count_start(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.operate)
        self.timer.start(20)

    def operate(self):
        self.update_send_buf()
        self.update_recv_buf()

class Candata():
    def __init__(self):
        self.ehub = EHub()
        self.sendval = 0
        print ("candata enter")

    def send_can_msg(self):
        global sendcnt
        global CanSendId
        global CanSendStr

        SendCanID = 0x10F00718
        data = [0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18]
        self.sendval +=1
        for i in range(8):
            data[7-i] = (self.sendval >> 8*i) & 0xFF
        CanSendStr= ''
        CanSendId = ''
        CanSendId += ("0x%X" % (SendCanID))
        for i in range(len(data)):
            #print ("send data = %d" % ( data[i]))
            CanSendStr += ("0x%02X, " % ( data[i]))
        self.ehub.send_can_frame(SendCanID, data)
        sendcnt += 1
    def recv_can_msg(self):
        global recvcnt
        global CanRecvStr
        global CanRecvId
        #print ("recv")
        std_id, ext_id, data = self.ehub.recv_can_frame()
        #print (" id = 0x%X" % ext_id)
        CanRecvId = ''
        if std_id != 0:
            CanRecvId += ("0x%X" % (std_id))
        else:
            CanRecvId += ("0x%X" % (ext_id))
        CanRecvStr = ''
        for i in range(len(data)):
            #print ("recv data = 0x%X" % ( data[i]))
            CanRecvStr += ("0x%02X, " % ( data[i]))
        recvcnt += 1

class WorkThread(QThread):
    trigger = pyqtSignal()
    can = Candata()
    def __int__(self):
        super(WorkThread,self).__init__()
    def run(self):
        while 1:
            self.can.recv_can_msg()
            #self.trigger.emit()         #循环完毕后发出信号

    def timer_start(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.operate)
        self.timer.start(100)

    def operate(self):
        self.can.send_can_msg()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    table = TableSheet()

    workThread=WorkThread()
    #workThread.trigger.connect(table.update_recv_buf)
    workThread.start()              #计时开始
    workThread.timer_start()
    table.show()
    sys.exit(app.exec_())



