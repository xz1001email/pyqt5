import numpy as np
import cv2
import screeninfo

from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys


# get the size of the screen
def video_screen_full():
    screen = screeninfo.get_monitors()[0]
    width, height = screen.width, screen.height

    window_name = 'projector'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)


#videopath='/home/xiao/FPGA/factory_test/fpga_factory_test/python/canreplayer/myplayvideo/rec_20180117_152908.mp4'
videopath='/home/xiao/FPGA/factory_test/fpga_factory_test/python/canreplayer/HW.avi'

def play_video():
    screen = screeninfo.get_monitors()[0]
    width, height = screen.width, screen.height
    window_name = 'projector'
    cv2.namedWindow(window_name, cv2.WND_PROP_FULLSCREEN)
    cv2.moveWindow(window_name, screen.x - 1, screen.y - 1)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)

    cap = cv2.VideoCapture(videopath)
    while (cap.isOpened()):
        ret, frame = cap.read()
        #cv2.imshow('frame', frame)
        cv2.imshow(window_name, frame)
        #if cv2.waitKey(40) & 0xFF == ord('q'):
        keyval = cv2.waitKey(40) & 0xFF
        if keyval == 0x1B or keyval == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    play_video()
    pass
