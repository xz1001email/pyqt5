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

can_data = {0,0,0,0,0,0}
ext_id = 0

global s_id_str
global s_data_str
s_data_str = ''
s_id_str = ''


def play_video():
    os.system("python3 cv_play_video.py")

class PlayThread(QThread):
    trigger = pyqtSignal()
    def __int__(self):
        super(PlayThread,self).__init__()

    def run(self):
        play_video()
        #self.trigger.emit()         #循环完毕后发出信号

ehub = None
class TableSheet(QWidget):
    sendcnt = 0
    recvcnt = 0
    sendval = 0
    playThread=PlayThread()
    def __init__(self):
        super().__init__()
        self.initUi()
        #self.create_button()

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

    def create_button(self):
        self.closeButton = QPushButton(self)
        self.closeButton.setText("play")          #text
        #self.closeButton.setIcon(QIcon("close.png")) #icon
        self.closeButton.setShortcut('Ctrl+D')  #shortcut key
        #self.closeButton.clicked.connect(self.close)
        self.closeButton.clicked.connect(self.playThread.start)
        self.closeButton.setToolTip("play video") #Tool tip
        self.closeButton.move(50,100)

    def _send_can_frame(self):
        SendCanID = 0x10F00718
        data = [0x11, 0x12, 0x13, 0x14, 0x15, 0x16, 0x17, 0x18]

        self.sendval +=1
        for i in range(8):
            data[7-i] = (self.sendval >> 8*i) & 0xFF

        data_str = ''
        id_str = ''
        id_str += ("0x%X" % (SendCanID))
        for i in range(len(data)):
            #print ("send data = %d" % ( data[i]))
            data_str += ("0x%02X, " % ( data[i]))

        ehub.send_can_frame(SendCanID, data)
        self.sendcnt += 1
        self.table.setItem(0,1,QTableWidgetItem(id_str))
        self.table.setItem(0,3,QTableWidgetItem(str(self.sendcnt)))
        self.table.setItem(0,4,QTableWidgetItem(data_str))

    def _recv_can_frame(self):
        ext_id, data = ehub.recv_can_frame()
        print (" id = 0x%X" % ext_id)

        data_str = ''
        id_str = ''
        id_str += ("0x%X" % (ext_id))
        for i in range(len(data)):
            #print ("data recv = 0x%x" % ( data[i]))
            #data_str += str(data[i])
            data_str += ("0x%X, " % ( data[i]))

        self.recvcnt += 1
        self.table.setItem(1,1,QTableWidgetItem(id_str))
        self.table.setItem(1,3,QTableWidgetItem(str(self.recvcnt)))
        self.table.setItem(1,4,QTableWidgetItem(data_str))
    def update_recv_buf(self):
        global s_id_str
        global s_data_str

        self.recvcnt += 1
        self.table.setItem(1,1,QTableWidgetItem(s_id_str))
        self.table.setItem(1,3,QTableWidgetItem(str(self.recvcnt)))
        self.table.setItem(1,4,QTableWidgetItem(s_data_str))

    def count_start(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.operate)
        #self.timer.start(1000)
        self.timer.start(20)


    def operate(self):
        #ehub.recv_can_frame()
        self._send_can_frame()
        #self._recv_can_frame()


def mesg_recv(name, fd):
    while 1:
        print (name)
        ext_id, data = fd.recv_can_frame()
        print (" id = 0x%X" % ext_id)

        data_str += ''
        id_str += ''
        id_str += ("0x%X" % (ext_id))
        for i in range(len(data)):
            #print ("data recv = 0x%x" % ( data[i]))
            #data_str += str(data[i])
            data_str += ("0x%X, " % ( data[i]))

class WorkThread(QThread):
    trigger = pyqtSignal()
    def __int__(self):
        super(WorkThread,self).__init__()

    def run(self):
        global s_id_str
        global s_data_str
        while 1:
            #table._recv_can_frame()
            #print ("recv")
            ext_id, data = ehub.recv_can_frame()
            #print (" id = 0x%X" % ext_id)

            s_id_str = ''
            s_id_str += ("0x%X" % (ext_id))
            s_data_str = ''
            for i in range(len(data)):
                #print ("recv data = 0x%X" % ( data[i]))
                s_data_str += ("0x%02X, " % ( data[i]))

            self.trigger.emit()         #循环完毕后发出信号


if __name__ == '__main__':


    app = QApplication(sys.argv)
    table = TableSheet()
    table.count_start()
    #table._recv_can_frame()
    #_thread.start_new_thread( mesg_recv, ("Thread-1", ehub))

    ehub = EHub()
    workThread=WorkThread()
    workThread.trigger.connect(table.update_recv_buf)
    workThread.start()              #计时开始
    table.show()
    sys.exit(app.exec_())

