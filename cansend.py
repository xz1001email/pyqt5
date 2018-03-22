#! /usr/bin/python
from ehub import EHub
from candata import ZlgCSV
import sys
import time
import getopt
import thread
import time

def usage(execname):
    usage = """
    Available option:
    -f  input file contains CAN frames to be replayed

    -d  select CAN device 0-CAN1  1-CAN2
    -v  verbose level
    -b  baudate: 1M/800K/500K...20K
    -s  send skip
    -c  max frame to sent
    -I  send CAN ID filter, 0x11E,0x3DB,..

    """
    print(execname + usage)
    sys.exit(1)
"""
def main(argv):
    input_file = ''
    data_source = None
    can_device = EHub.CAN_DEV_0
    verbose = 0
    send_skip = 0;
    send_count = 0
    can_id_filter = []
    baudrate = EHub.CAN_SPEED_500K
    print "main enter"
    try:
        opts, args = getopt.getopt(argv[1:], "f:d:v:b:c:I:s:")
    except getopt.GetoptError:
        usage(argv[0])

    for opt, arg in opts:
        if "-f" == opt:
            input_file = arg
        if "-d" == opt:
            can_device = int(arg)
        if "-v" == opt:
            verbose = int(arg)
        if "-s" == opt:
            send_skip = int(arg)
        if "-c" == opt:
            send_count = int(arg)
        if "-I" == opt:
            id_str = arg.split(',')
            for a_id in id_str:
                can_id_filter.append(int(a_id, 16))
        if "-b" == opt:
            for i in range(len(EHub.BAUDRATE_NAMES)):
                if EHub.BAUDRATE_NAMES[i].endswith(arg):
                    baudrate = i

    print "Init CAN device " + str(can_device) + ", baudrate " + EHub.BAUDRATE_NAMES[baudrate]
    ehub = EHub()
    ehub.config_can_device(can_device, baudrate);

    id = 0x10F00718;
    ext = ehub.CAN_ID_EXT;
    data = [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8];

    #ehub.send_can_frame(id, can_device, ext, data);

    try:
        thread.start_new_thread( pthread_can_send, ("can_write", 1, ) )
        thread.start_new_thread( pthread_can_recv, ("can_read", 1, ) )
    except:
        print "Error: unable to start thread"

while 1:
    #print "end"
    pass

if __name__ == '__main__':
    main(sys.argv)
"""







def pthread_can_send( threadName, delay):
    count = 0
    ehub = EHub()
    print "%s: enter!\n" % (threadName)

    id = 0x10F00718;
    ext = ehub.CAN_ID_EXT;
    data = [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8];
    can_device = EHub.CAN_DEV_0

    while 1:
        ehub.send_can_frame(id, can_device, ext, data);
        count += 1
        print "%s: %s" % ( str(count), time.ctime(time.time()) )
        time.sleep(delay)



def pthread_can_recv( threadName, delay):
    count = 0
    ehub = EHub()
    print "%s: enter!\n" % (threadName)

    id = 0x10F00718;
    ext = ehub.CAN_ID_EXT;
    data = [0x1, 0x2, 0x3, 0x4, 0x5, 0x6, 0x7, 0x8];
    can_device = EHub.CAN_DEV_0

    while 1:
        ehub.recv_can_frame(id, can_device, ext, data);
        count += 1
        print "%s: %s" % ( str(count), time.ctime(time.time()) )
        time.sleep(delay)



try:
    thread.start_new_thread( pthread_can_recv, ("can_read", 1, ) )
    #thread.start_new_thread( pthread_can_send, ("can_write", 1, ) )
except:
    print "Error: unable to start thread"

while 1:
    #print "end"
    pass
