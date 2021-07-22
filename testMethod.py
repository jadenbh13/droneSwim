
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
import matplotlib.pyplot as plt

xV = [0]
yV = [0]
start = time.time()
mn = 0
front = True
cycleN = 20
m = 0
prevNum = 0
xPos = 0.5
yPos = 0
mnY = 0
def testSin(cf, real, im):
	global front
	global mn
	global cycleN
	global prevNum
	global mnY
	currNum = (mn % (2 * math.pi))
	if front == True:
		mn += 0.0001
		if mn > ((2 * math.pi) - 0.001):
			cycleN += 1
			mn = 0
	prevNum = (mn % (2 * math.pi))
	amp = (cycleN + 1) / 10
	desAngle = 30
	rads = (mn + math.radians(90))
	x = amp * ((math.sin(rads)))
	y = amp * ((math.cos(rads)))
	mnY = amp * ((math.cos(mn)))
	if y < 0:
		y = 0
	if y != 0:
		ang = math.degrees(math.atan2(x,y))
		if abs(ang) < (desAngle / 2):
			print(ang)
			#leT = ledTiming(real, im, tm)
			#setLed(cf, leT[0], leT[1], leT[2])
	xs = (x)
	#print(mn)
	#print(cycleN)
	print((xs / 10), (y / 10))
	time.sleep(0.0001)
	return xs, y

def testSin2(cf, real, im):
	global front
	global mn
	global cycleN
	global prevNum
	global xPos
	global yPos
	currNum = (mn % (2 * math.pi))
	if mn > ((2 * math.pi) - 0.001):
		cycleN += 1
		mn = 0
	if front == True:
		mn += 0.0008
	if front == False:
		mn -= 0.0008
	prevNum = (mn % (2 * math.pi))
	amp = (cycleN + 1) / 10
	desAngle = 30
	tm = time.time()
	rads = (mn + math.radians(90))
	x = amp * ((math.sin(rads)))
	y = amp * ((math.cos(rads)))
	if y < 0:
		y = 0
	if y != 0:
		ang = math.degrees(math.atan2(x,y))
		if abs(ang) < (desAngle / 2):
			print(ang)
			xPos = x
			yPos = y
			#leT = ledTiming(real, im, tm)
			#setLed(cf, leT[0], leT[1], leT[2])
		else:
			k = 0
			#setLed(cf, 0, 0, 0)
	else:
		k = 0
		#setLed(cf, 0, 0, 0)
	xs = (xPos)
	ys = (yPos)
	#print(mn)
	print(cycleN)
	print((xs / 10), (ys / 10))
	time.sleep(0.0001)
	return xs, ys


def testSin3(cf, real, im):
	global front
	global mn
	global cycleN
	global prevNum
	global mnY
	currNum = (mn % (2 * math.pi))
	addNum = 0.00005
	if mn > ((2 * math.pi) - 0.001):
		mn = 0
	if front == True:
		mn += addNum
	if front == False:
		mn -= addNum
	prevNum = (mn % (2 * math.pi))
	amp = (cycleN + 1) / 10
	desAngle = 70
	rads = (mn + math.radians(0))
	x = amp * ((math.sin(rads)))
	y = amp * ((math.cos(rads)))
	mnY = amp * ((math.cos(mn)))
	"""if mn > 285:
		front = False
	elif mn < 255:
		front = True"""
	if y < 0:
		y = 0
	ang = math.degrees(math.atan2(x,y))
	degAng = 70
	print(ang)
	if ang != 90.0 or ang != -90.0:
		if front == True:
			if ang > (degAng / 2):
				front = False
				cycleN += 1
		if front == False:
			if ang < (0 - (degAng / 2)):
				front = True
				cycleN += 1
	print(x, y, cycleN)
	time.sleep(0.0001)
	return x, y
while True:
	nb = testSin3(2, 1, 2)
	if cycleN == 30:
		print("   ")
		print(mnY)
		print("   ")
		break
