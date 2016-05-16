#!/usr/bin/env python

'''
    socklidar.py
    Author: Karel De Coster (k.decoster94@gmail.com)
    Github: http://github.com/kareldecoster/socklidar
    Date: 2016-5-16

    Adapted from lidar.py downloaded from 

      http://www.getsurreal.com/products/xv-lidar-controller/xv-lidar-controller-visual-test

    Copyright (C) 2016 Simon D. Levy

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Lesser General Public License as 
    published by the Free Software Foundation, either version 3 of the 
    License, or (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
'''

import threading, time, traceback, os, socket, sys, struct, math, numpy

class socklidar(object):

    def __init__(self, com_port):
        self.server_address = ("192.168.7.1", 1234)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.thread = threading.Thread(target=self._read_lidar, args=())
        self.thread.daemon = False
        self.state = 0
        self.timestamp = 0
        self.exitflag = 0
        self.index = 0
        self.lidar_data = [()]*360 # 360 elements (distance,quality), indexed by angle
        self.connection = 0
        self.thread.start()


    def set_exitflag(self):
        '''
        Raises the exitflag so thread can exit gracefully.
        '''
        self.exitflag = 1

    def getScan(self):
        '''
        Returns 360 (distance, quality) tuples.
        '''
        return [pair if len(pair) == 2 else (0,0) for pair in self.lidar_data]

    def _read_lidar(self):

        nb_errors = 0
        while self.exitflag == 0:
            try:
                if self.state == 0 :
                    self.sock.bind(self.server_address)
                    self.sock.listen(1)
                    self.state = 1

                if self.state == 1 :
                    self.connection, client_address = self.sock.accept()
                    self.state = 2

                elif self.state == 2 :

                    time = struct.unpack("<I", self.connection.recv(4))[0]
                    if( time >= self.timestamp):
                        # update time
                        self.timestamp = time

                        # update position to files
                        x = struct.unpack("d", self.connection.recv(8))[0]
                        y = struct.unpack("d", self.connection.recv(8))[0]
                        xstr = '%.5f' % x
                        ystr = '%.5f' % y
                        fx = open("/var/lib/mercator/x", "w")
                        fy = open("/var/lib/mercator/y", "w")
                        fx.write(xstr)
                        fy.write(ystr)
                        fx.close()
                        fy.close()

                        # update scan
                        angle = 0
                        while (angle < 360):
                            distance = struct.unpack("d", self.connection.recv(8))[0]
                            if( distance < 0.001 or numpy.isnan(distance)) :
                                distance = 0
                            self.lidar_data[angle] = (round(float(distance)),10)
                            angle += 1

                    else:
                        self.connection.recv(8*362)
                        #read old value.. should never happen...
                        print "Old values received!"

                else: # default, should never happen...
                    self.state = 0

            except:
                traceback.print_exc()
                exit(0)
        #End of while loop. Exit gracefully
        exit(0)    
