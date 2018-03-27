#! /usr/bin/python
import struct
import sys
import os

class EHub:
    ehub_fd = None
    def __init__(self):
        EHUB_USB_VID = "0483"
        EHUB_USB_PID = "003B"
        """
        /sys/bus/hid/devices/0003\:0483\:5750.003B/hidraw/hidraw1/dev
        /sys/class/hidraw/hidraw?
        """
        hidrawx = ""
        sys_hidraw = "/sys/class/hidraw/hidraw"
        for x in range(4):
            if os.path.islink(sys_hidraw + str(x) + "/device"):
                #print( "Test " + sys_hidraw + str(x))
                if EHUB_USB_VID in os.readlink(sys_hidraw + str(x) + "/device"):
                    hidrawx = "/dev/hidraw" + str(x)
                    break;

        if 0 == len(hidrawx):
            print ("EHub hidraw device file not found, make sure it's connected")
            sys.exit(1)
        if not os.path.exists(hidrawx):
            print ("Hidraw device " + hidrawx + " not exist")
            sys.exit(1)

        try:
            self.ehub_fd = open(hidrawx, "rb+")
        except IOError:
            print ("open " + hidrawx + \
                " failed, make sure file exist and write permission allowed")
            sys.exit(1)
        print ("init EHub from " + hidrawx)

    USB_MESG_DATA_SIZE	= 60
    CMD_CONFIG_CAN      = 0x80
    CMD_SEND_CAN_FRAME  = 0x81
    CMD_START_CAPTURE  = 0x55
    CMD_STOP_CAPTURE  = 0x66
    CAN0_DATA = 0x11
    def pack_usb_msg(self, cmd):
        """
        typedef struct
        {
            uint8_t cmd;
            uint8_t id;
            int16_t size;
            uint8_t data[USB_MESG_DATA_SIZE];
        }USB_MESSAGE;
        """
        return struct.pack("BBH", cmd, 0, 0)

    def unpack_usb_msg(self, msg):
        head = struct.unpack("BBH", msg)
        print (head)

    BAUDRATE_NAMES = (
        "CAN_SPEED_INVALID",
        "CAN_SPEED_1M",
        "CAN_SPEED_800K",
        "CAN_SPEED_500K",
        "CAN_SPEED_250K",
        "CAN_SPEED_125K",
        "CAN_SPEED_100K",
        "CAN_SPEED_50K",
        "CAN_SPEED_20K",
        "CAN_SPEED_10K",
        "CAN_SPEED_5K",
        "CAN_SPEED_MAX")
    CAN_SPEED_INVALID,\
        CAN_SPEED_1M,\
        CAN_SPEED_800K,\
        CAN_SPEED_500K,\
        CAN_SPEED_250K,\
        CAN_SPEED_125K,\
        CAN_SPEED_100K,\
        CAN_SPEED_50K,\
        CAN_SPEED_20K,\
        CAN_SPEED_10K,\
        CAN_SPEED_5K,\
        CAN_SPEED_MAX = range(12)

    CAN_BAUDRATE_IDX_SCALE, \
        CAN_BAUDRATE_IDX_SJW, \
        CAN_BAUDRATE_IDX_TS1, \
        CAN_BAUDRATE_IDX_TS2 = range(4)

    CAN_BAUDRATE_PARAM = (
        (8,     0x0,    0x6,    0x0),#CAN_SPEED_INVALID,
        (4,     0x0,    0x6,    0x0),#CAN_SPEED_1M,
        (5,     0x0,    0x6,    0x0),#CAN_SPEED_800K,
        (8,     0x0,    0x6,    0x0),#CAN_SPEED_500K,
        (16,    0x0,    0x6,    0x0),#CAN_SPEED_250K,
        (32,    0x0,    0x6,    0x0),#CAN_SPEED_125K,
        (40,    0x0,    0x6,    0x0),#CAN_SPEED_100K,
        (80,    0x0,    0x6,    0x0),#CAN_SPEED_50K,
        (200,   0x0,    0x6,    0x0),#CAN_SPEED_20K,
        (400,   0x0,    0x6,    0x0),
        (800,   0x0,    0x6,    0x0))
    def config_can_device(self, dev, baudrate):
        """
        typedef struct {
            unsigned short   prescaler;
            unsigned char    sjw;
            unsigned char    ts1;
            unsigned char    ts2;
            uint8_t          dev;
        } ConfigCanInfo;
        """
        bp = self.CAN_BAUDRATE_PARAM[baudrate]
        usb_msg = self.pack_usb_msg(self.CMD_CONFIG_CAN)
        usb_msg += struct.pack("HBBBB",
                bp[self.CAN_BAUDRATE_IDX_SCALE],
                bp[self.CAN_BAUDRATE_IDX_SJW],
                bp[self.CAN_BAUDRATE_IDX_TS1],
                bp[self.CAN_BAUDRATE_IDX_TS2],
                dev)
        self.write(usb_msg)

    CAN_DEV_0   = 0
    CAN_DEV_1   = 1
    CAN_ID_STD  = 0
    CAN_ID_EXT  = 1
    CAN_ID_STD_MAX  = 0x7FF
    CAN_ID_EXT_MAX  = 0x1FFFFFFF
    def send_can_frame(self, id, data):
        """
        typedef struct {
            uint32_t    id;
            uint8_t     dev:1;
            uint8_t     ext:1;
            uint8_t     len:6;
            uint8_t     data[8];
        } SendCanFrame;
        """
        dev = self.CAN_DEV_0
        ext = self.CAN_ID_EXT
        datalen = 8
        canlen = 13
        if self.CAN_ID_STD == ext and id > self.CAN_ID_STD_MAX or\
            self.CAN_ID_EXT == ext and id > self.CAN_ID_EXT_MAX:
            print ("Invalid CAN ID " + str(id))

        #pack usb header
        usb_msg = struct.pack("BBH", self.CMD_SEND_CAN_FRAME, 0, canlen)

        bitfiels = dev | ext << 1 | datalen << 2;
        usb_msg += struct.pack("IB", id, bitfiels)

        for i in range(8):
            usb_msg += struct.pack("B", data[i]);

        self.write(usb_msg)

    def write(self, usb_msg):
        """
        padding = 0;
        if len(usb_msg) > self.USB_MESG_DATA_SIZE:
            return -1
        else:
            padding = self.USB_MESG_DATA_SIZE - len(usb_msg)
        for i in range(padding):
            usb_msg += struct.pack("B", 0)
        """
        self.ehub_fd.write(usb_msg)
        self.ehub_fd.flush()

    def recv_can_frame(self):
        data = [1,2,3,4,5,6,7,8];
        canid = 0
        bitfiels = 0

        UsbDataLen = 64
        offset = 0
        recvbit = self.ehub_fd.read(UsbDataLen)
        recvlen = len(recvbit)
        print (recvlen)

        #for i in range(recvlen):
        #    print ("0x%x" % struct.unpack("B", recvbit[i:i+1]))

        cmd, idx, datalen = struct.unpack("BBH", recvbit[0 : 4])
        offset += 4

        std_id, ext_id = struct.unpack("II", recvbit[offset : offset+8])
        print ("std_id = 0x%x, ext_id = 0x%x\n" % (std_id, ext_id))
        offset += 8

        IDE, RTR, DLC = struct.unpack("BBB", recvbit[offset : offset+3])
        print ("IDE = 0x%x, RTR = 0x%x, DLC = 0x%x" % (IDE, RTR, DLC))
        offset += 3

        for i in range(8):
            a=i+offset
            b=i+offset+1
            data[i] = struct.unpack("B", recvbit[a:b])
            print (a, b, "0x%x" % data[i])

        return ext_id, data


    def send_cmd_to_ehub(self, cmd):
        """
        typedef struct {
            uint32_t    id;
            uint8_t     dev:1;
            uint8_t     ext:1;
            uint8_t     len:6;
            uint8_t     data[8];
        } SendCanFrame;
        """

        data = [1,2,3,4,5,6,7,8];
        id = 0x11223344
        dev = self.CAN_DEV_0
        ext = self.CAN_ID_EXT
        if self.CAN_ID_STD == ext and id > self.CAN_ID_STD_MAX or\
            self.CAN_ID_EXT == ext and id > self.CAN_ID_EXT_MAX:
            print ("Invalid CAN ID " + str(id))

        usb_msg =  self.pack_usb_msg(cmd)
        data_len = len(data)

        bitfiels = dev | ext << 1 | data_len << 2;
        usb_msg += struct.pack("IB", id, bitfiels)
        for i in range(data_len):
            usb_msg += struct.pack("B", data[i]);
        self.write(usb_msg)


