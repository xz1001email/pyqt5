#coding=utf-8

import cv2.cv as cv
filename = "test.avi"
win_name = "video player"
capture = cv.CaptureFromFile(filename)
cv.NamedWindow(win_name, cv.CV_WINDOW_AUTOSIZE)

# 定义一个无限循环
while 1:

       # 每次从视频数据流框架中抓取一帧图片
    image = cv.QueryFrame(capture)

    # 将图片显示在特定窗口上
    cv.ShowImage(win_name, image)

    # 当安县Esc键时退出循环
    c = cv.WaitKey(33)
    if c == 27:
        break

# 退出循环后销毁显示窗口
cv.DestroyWindow(win_name)
