#!/usr/bin/env python

'''
rplidarplot.py : A little Python class to display scans from the RP Lidar
             
Author: Karel De Coster (k.decoster94@gmail.com)
Github: http://github.com/kareldecoster/RPLidar
Date: 2016-4-7

Based on XVlidar by Simon D. Levy (http://github.com/simondlevy/xvlidar).

This code is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as 
published by the Free Software Foundation, either version 3 of the 
License, or (at your option) any later version.

This code is distributed in the hope that it will be useful,     
but WITHOUT ANY WARRANTY without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this code.  If not, see <http://www.gnu.org/licenses/>.
'''


# XVLIDAR-04LX specs
RPLIDAR_MAX_SCAN_DIST_MM    = 6000
RPLIDAR_DETECTION_DEG       = 360
RPLIDAR_SCAN_SIZE           = 360

from socklidar import socklidar

from math import sin, cos, radians
import time
from sys import exit, version
import signal
import sys

#GLOBALS
done = 0

def signal_handler(signal, frame):
        global done 
        done = 1


if version[0] == '3':
    import _thread as thread
else:
    import thread

if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal_handler)
    lidar = socklidar()
    while done == 0 :
        time.sleep(1)
        distances = [pair[0] for pair in lidar.getScan()]
        
        print " New Scan :    angle |   distance"
        i = 0
        while i < 360:
            print "           {angle} | {distance}".format(angle = i, distance = distances[i])
            i = i+1

    lidar.set_exitflag()
    print""
    print "DONE"
        
