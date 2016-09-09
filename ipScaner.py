#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  9 15:30:26 2016

@author: eric zeng
"""
import time
import platform
import os
import threading

def ipAlive(ipStr):
    cmd = []
    pform = platform.system()
    if pform == "Windows":
        cmd = ['ping -n 1',ipStr]                   #eg:ping -n 1 192.168.0.1
    else:
        cmd = ['ping -c 1',ipStr]
    output = os.popen(" ".join(cmd)).readlines()    #catch returned ping-string
    
    flag = False
    for line in list(output):
        if not line:
            continue                               #sleeping ip
        if str(line).upper().find("TTL") >= 0:
            flag = True                            #alive ip
            break
    if flag:
        print("ip:%s is alive ***" % ipStr)

def ipScaner():
    print("Pls enter IP address: ")
    ip = input().strip()
    print("\nStart time %s" % time.ctime())
    iplist = ip.split(".")
    #prefix = 192.168.0
    if len(iplist) != 4:
        print("Wrong ip format,please check %s" % ip)
    else:
        prefix = '.'.join(ip.split(".")[:-1])
    for i in range(1,10):
        ip = "%s.%s" % (prefix,i)
        threading.Thread(target = ipAlive(ip))
        time.sleep(0.3)
    print("End time %s" % time.ctime())
    
if __name__ == '__main__':
    ipScaner()
