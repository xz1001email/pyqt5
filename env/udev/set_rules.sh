
!#/bin/sh

#add scaner group
#lsusb 查看设备厂商ID
#添加USB设备 到  scanner Group

cp 40-scanner.rules /etc/udev/rules.d/

sudo /etc/init.d/udev restart


