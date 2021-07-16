
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.log import LogConfig
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger
from cflib.utils import uri_helper
from cflib.crazyflie.mem import MemoryElement
import math
import cmath
import pygame
from math import sin,cos,radians
import random
import threading

start = time.time()
mn = 0
front = True
cycleN = 0
def sins(real, im):
    global front
    global mn
    global cycleN
    if front == True:
        mn += 0.0001
        if mn > (2 * math.pi):
            front = False
    elif front == False:
        mn -= 0.0001
        if mn < 0:
            cycleN += 1
            front = True
    print(mn / 10)
    #print(mn / 10)
    print("  ")
    phs = 0
    tb = abs(math.sqrt((real ** 2) + (im ** 2)))
    amp = 1
    f = 80
    tn = math.atan(im / real)
    #print(tn)
    sig = (amp * ((math.sin((2 * math.pi) * f * ((mn / 30) + tn)))))
    #print(sig / 10)
    print(cycleN)
    print(sig / 10)
    ti = 1
    time.sleep((0.001) * ti)
    return (mn / 10), (sig / 10)
    #cf.commander.send_stop_setpoint()
while True:
    sins(1, 2)
