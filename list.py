#-*- coding:utf-8 -*-
'''
TableWidget
'''
__author__ = 'Tony Zhu'
import sys
import time
#import _thread
from PyQt5.QtCore import  Qt
from PyQt5.QtWidgets import QWidget, QApplication, QLabel,  QTableWidget,QHBoxLayout, QTableWidgetItem, QComboBox,QFrame,QDesktopWidget
from PyQt5.QtGui import QFont,QColor,QBrush,QPixmap
from PyQt5.QtCore import QTimer

#from cansend import Ectrl
from ehub import EHub

class TableSheet(QWidget):
    ehub = None
    age = 0
    def __init__(self):
        super().__init__()
        self.initUi()
        self.ehub = EHub()

    def initUi(self):
        horizontalHeader = ["工号","姓名","性别","年龄","职称"]
        self.setWindowTitle('TableWidget Usage')
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setRowCount(2)

        self.table.setHorizontalHeaderLabels(horizontalHeader)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectColumns)
        self.table.setSelectionMode(QTableWidget.SingleSelection  )

        for index in range(self.table.columnCount()):
            headItem = self.table.horizontalHeaderItem(index)
            headItem.setFont(QFont("song", 12, QFont.Bold))
            headItem.setForeground(QBrush(Qt.gray))
            headItem.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)

        self.table.setColumnWidth(4,200)
        self.table.setRowHeight(0,40)
        #self.table.setFrameShape(QFrame.HLine)#设定样式
        #self.table.setShowGrid(False) #取消网格线
        #self.table.verticalHeader().setVisible(False) #隐藏垂直表头

        self.table.setItem(0,0, QTableWidgetItem("001"))
        self.table.setItem(0,1,QTableWidgetItem("Tom"))
        genderComb = QComboBox()
        genderComb.addItem("男性")
        genderComb.addItem("女性")
        genderComb.setCurrentIndex(0)
        self.table.setCellWidget(0,2,genderComb)
        self.table.setItem(0,3,QTableWidgetItem("30"))
        self.table.setItem(0,4,QTableWidgetItem("产品经理"))

        self.table.setItem(1,0, QTableWidgetItem("005"))
        self.table.setItem(1,1,QTableWidgetItem("Kitty"))
        genderComb = QComboBox()
        genderComb.addItem("男性")
        genderComb.addItem("女性")
        genderComb.setCurrentIndex(1)
        self.table.setCellWidget(1,2,genderComb)
        self.table.setItem(1,3,QTableWidgetItem("24"))
        self.table.setItem(1,4,QTableWidgetItem("程序猿安慰师"))

        row_count = self.table.rowCount()
        self.table.insertRow(row_count)
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.table)
        self.setLayout(mainLayout)
        self.setGeometry(300, 300, 600, 200)
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

    def _send_can_frame(self):
        SendCanID = 0x10F00718
        data = [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8]
        self.ehub.send_can_frame(SendCanID, data)
        return 0


    def count_start(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.operate)
        self.timer.start(2000)


    def operate(self):
        if 0 == self._send_can_frame():
            #self.ehub.recv_can_frame()
            self.age += 1
            self.table.setItem(0,3,QTableWidgetItem(str(self.age)))



if __name__ == '__main__':


    app = QApplication(sys.argv)
    table = TableSheet()
    table.show()
    table.count_start()
    sys.exit(app.exec_())

