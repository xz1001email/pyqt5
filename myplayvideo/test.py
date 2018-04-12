import numpy as np
import cv2
import screeninfo

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys



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


# get the size of the screen
def video_screen_full():
    screen = screeninfo.get_monitors()[0]
    width, height = screen.width, screen.height

    window_name = 'projector'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)


def play_video():
    cap = cv2.VideoCapture('./rec_20180117_152908.mp4')
    while (cap.isOpened()):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        #cv2.imshow(window_name, frame)
        #if cv2.waitKey(40) & 0xFF == ord('q'):
        if cv2.waitKey(40) & 0xFF == 0x1B:
            break
        cap.release()
        cv2.destroyAllWindows()

class WorkThread(QThread):
    def __int__(self):
        super(WorkThread,self).__init__()

    def run(self):
        play_video()

class PushButton(QWidget):
    trigger = pyqtSignal()
    def __init__(self):
        super(PushButton,self).__init__()
        self.initUI()

    def send_signal():
        self.trigger.emit()         #循环完毕后发出信号

    def initUI(self):
        self.setWindowTitle("PushButton")
        self.setGeometry(400,400,300,260)

        self.closeButton = QPushButton(self)
        self.closeButton.setText("play")          #text
        #self.closeButton.setIcon(QIcon("close.png")) #icon
        self.closeButton.setShortcut('Ctrl+D')  #shortcut key
        #self.closeButton.clicked.connect(self.close)
        self.closeButton.clicked.connect(workThread.start)
        self.closeButton.setToolTip("Close the widget") #Tool tip
        self.closeButton.move(50,100)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PushButton()

    workThread=WorkThread()
    workThread.start()              #计时开始

    ex.show()
    sys.exit(app.exec_())


