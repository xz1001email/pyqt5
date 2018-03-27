#! /usr/bin/python
from ehub import EHub
#from candata import ZlgCSV
import sys
import time
import getopt
#import thread
import _thread
import time


class Ectrl:
    ehub = None
    def __init__(self):
        ehub = EHub()

    def recv_can_frame_cnt(self):
        count = 0
        ehub.recv_can_frame()
        count += 1
        return count

    def send_can_frame(self):
        SendCanID = 0x10F00718
        data = [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8]
        ehub.send_can_frame(SendCanID, data)
        return 0







'''
def pthread_can_send( threadName, delay ):
    count = 0
    ehub = EHub()
    print ("%s: enter!\n" % (threadName))

    #ext = ehub.CAN_ID_EXT;
    #can_device = EHub.CAN_DEV_0

    SendCanID = 0x10F00718;
    data = [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8];

    #ehub.send_cmd_to_ehub(ehub.CMD_START_CAPTURE);
    while 1:
        ehub.send_can_frame(SendCanID, data);
        count += 1
        print ("%s: count: %d, %s\n" % (threadName,  (count), time.ctime(time.time()) ))
        ehub.recv_can_frame()
        time.sleep(delay)



def pthread_can_recv( threadName, delay ):
    count = 0
    ehub = EHub()
    print ("%s: enter!\n" % (threadName))

    #id = 0x10F00718;
    id = 0x11223344;
    ext = ehub.CAN_ID_EXT;
    data = [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8];
    can_device = EHub.CAN_DEV_0

    while 1:
        #ehub.recv_can_frame();
        ehub.read();
        count += 1
        print ("%s: count: %d, %s" % (threadName,  (count), time.ctime(time.time()) ))
       # time.sleep(delay)



try:
    #ehub = EHub()
    #ehub.capture_control( ehub.CMD_START_CAPTURE, ehub.CAN1_DATA)

    #thread.start_new_thread( pthread_can_recv, ("can_read", 1, ) )
    _thread.start_new_thread( pthread_can_send, ("can_write", 1, ) )
except:
    print ("Error: unable to start thread")

while 1:
    #print ("end")
    pass

'''


