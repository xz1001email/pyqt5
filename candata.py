#! /usr/bin/python
#coding=utf8
from ehub import EHub
class ZlgCSV:
    cvs_file = None

    def __init__(self, cvs):
        self.cvs_file = open(cvs, "r")

    CSV_COL_NO, CSV_COL_DIR, CSV_COL_TIME, CSV_COL_ID,\
        CSV_COL_FORMAT, CSV_COL_TYPE, CSV_COL_LEN, CSV_COL_DATA = range(8)
    CAN_STD_ID_STR = "标准帧".decode("utf8")
    CAN_EXT_ID_STR = "扩展帧".decode("utf8")

    CAN_DIR_READ_STR  = "接收".decode("utf8")
    CAN_DIR_WRITE_STR = "发送".decode("utf8")
    def read_can_frame(self):
        line = None
        fields = None
        id = 0
        data = ()


        #Read out the CSV header
        line = self.cvs_file.readline()

        line_count = 1;
        while 1:
            line = self.cvs_file.readline().decode("gbk")
            if 0 == len(line):
                break;
            #print "Line#" + str(line_count) + "|" + line

            fields = line.split(',')
            id = int(fields[self.CSV_COL_ID].split(' ')[0], 16)

            dir_str = fields[self.CSV_COL_DIR].strip()
            if self.CAN_DIR_WRITE_STR == dir_str:
                print "Ignore received CAN message"
                continue

            data_str = fields[self.CSV_COL_DATA].strip().split(' ')
            data = []
            for i in range(len(data_str)):
                data.append(int(data_str[i], 16))
            
            time = float(fields[self.CSV_COL_TIME].strip())

            std_can = True
            ext = EHub.CAN_ID_STD
            format_str = fields[self.CSV_COL_FORMAT].strip()
            if self.CAN_STD_ID_STR == format_str:
                std_can = True
                ext = EHub.CAN_ID_STD
            elif self.CAN_EXT_ID_STR == format_str:
                std_can = False
                ext = EHub.CAN_ID_EXT
            else:
                assert(0)
            line_count += 1
            yield (time, id, ext, data)

    def next_record(self):
        pass
