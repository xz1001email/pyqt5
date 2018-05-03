

#Set "priority=100" for gcc-4.9 and "priority=50" for gcc-5.
#sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-4.9 100
#sudo update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-5.0 50

#Set "priority=100" for g++-4.9 and "priority=50" for g++-5.
#sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-4.9 100
#sudo update-alternatives --install /usr/bin/g++ g++ /usr/bin/g++-5.0 50

#check
#Verify the priority settings using:
#update-alternatives --query gcc
#update-alternatives --query g++




sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 100
sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 50


#sudo update-alternatives --config python
