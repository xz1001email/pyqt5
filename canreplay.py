#! /usr/bin/python
from ehub import EHub
from candata import ZlgCSV
import sys
import time
import getopt

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

def main(argv):
    input_file = ''
    data_source = None
    can_device = EHub.CAN_DEV_0
    verbose = 0
    send_skip = 0;
    send_count = 0 
    can_id_filter = []
    baudrate = EHub.CAN_SPEED_500K
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

    if 0 == len(input_file):
        print "No input file given"
        usage(argv[0])

    if input_file.endswith(".csv") or input_file.endswith(".CSV"):
        data_source = ZlgCSV(input_file)
    else:
        print "Unknown file format " + input_file + ", we only support ZhouLiGon CSV file"
        sys.exit(1)

    print "Init CAN device " + str(can_device) + ", baudrate " + EHub.BAUDRATE_NAMES[baudrate]
    ehub = EHub()
    ehub.config_can_device(can_device, baudrate);

    count = 0;
    sent  = 0;
    last_frame_time = 0;
    frames = data_source.read_can_frame()
    for frame in frames:
        count += 1; 
        if (0 != send_skip and count < send_skip):
            continue;

        (ts, id, ext, data) = frame
        if last_frame_time > 0:
            if verbose > 2:
                print "sleep " + str((ts - last_frame_time))
            time.sleep(ts - last_frame_time)
            pass

        if 0 == len(can_id_filter) or id in can_id_filter:
            ehub.send_can_frame(id, can_device, ext, data)
            if verbose > 0:
                print "Seding Frame#" + str(count) + " ID:" + str(id) + " Data" + str(data)
            sent += 1
        elif verbose > 2:
            print "Filter Frame#" + str(count) + " ID:" + str(id) + " Data" + str(data)

        last_frame_time = ts 
        if 0 != send_count and sent > send_count:
            break;

if __name__ == '__main__':
    main(sys.argv)

