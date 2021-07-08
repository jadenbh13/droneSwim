
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
import numpy as np

def sec(numbers):
	m1 = m2 = float('inf')
	for x in numbers:
		if x <= m1:
			m1, m2 = x, m1
		elif x < m2:
			m2 = x
	return m2

def closest(numb):
	close = []
	closeR = []
	newDeg = []
	degArr = [0, 90, 180, 270, 360]
	for t in degArr:
		un = abs(t - numb)
		closeR.append(un)
	nv = min(closeR)
	#print(nv)
	numbs = 0
	if numb < 1000:
		h = 0
		secondArr = []
		#print(closeR)
		while h < len(closeR):
			if closeR[h] == min(closeR):
				close += [h]
			if closeR[h] == sec(closeR):
				close += [h]
			h += 1
	"""else:
		h = 0
		while h < len(closeR):
			if closeR[h] == max(closeR):
				close += [h]
			h += 1"""
	twoArr = []
	for g in close:
		twoArr += [degArr[g]]
	realTwo = list(dict.fromkeys(twoArr))
	return sorted(realTwo)

def perCol(col1, col2, per1, per2):
	newCol1 = []
	newCol2 = []
	for t in col1:
		j = t * per1
		newCol1 += [j]

	for k in col2:
		m = k * per2
		newCol2 += [m]
	finalCol = []
	v = 0
	while v < len(newCol1):
		jh = 2 * ((newCol1[v] + newCol2[v]) / 2)
		finalCol += [jh]
		v += 1
	return finalCol

def getRgb(inp):
	mnArr = closest(inp)
	firLis = mnArr
	index = min(mnArr, key=lambda x:abs(x-inp))
	inX = 0
	nonInx = 0
	d = 0
	while d < len(mnArr):
		if mnArr[d] == index:
			inX = d
		else:
			if d < 2:
				nonInx = d
		d += 1
	base = firLis[0]
	bigNum = firLis[1] - base
	per = (inp - base) / bigNum
	per2 = 1.0 - per
	col1 = []
	col2 = []
	newCol = []
	perL = [per, per2]
	maxP = max(perL)
	minP = min(perL)
	i = 0
	while i < len(mnArr):
		if i == 0:
			if mnArr[i] == 0:
				col1 = [0, 255, 0]
			if mnArr[i] == 90:
				col1 = [255, 255, 0]
			if mnArr[i] == 180:
				col1 = [255, 0, 0]
			if mnArr[i] == 270:
				col1 = [0, 0, 255]
			if mnArr[i] == 360:
				col1 = [0, 255, 0]
		elif i == 1:
			if mnArr[i] == 0:
				col2 = [0, 255, 0]
			if mnArr[i] == 90:
				col2 = [255, 255, 0]
			if mnArr[i] == 180:
				col2 = [255, 0, 0]
			if mnArr[i] == 270:
				col2 = [0, 0, 255]
			if mnArr[i] == 360:
				col2 = [0, 255, 0]

		i += 1
	colL = [col1, col2]
	"""print(mnArr)
	print(colL[inX])
	print(maxP)
	print(colL[nonInx])
	print(minP)"""
	finalColour = perCol(colL[inX], colL[nonInx], maxP, minP)
	return finalColour


def ledTiming(x, y, ts):
	W = complex(1000, 1000) # Define fourier operator with x and y input
	newP = 0

	mag = 0
	o = math.pi/180 # Degree symbol
	p = 0


	mag = abs(W) # get magnitude (increases as antenna gets closer to wire)
	print("	")
	p = 180 - ((cmath.phase(W))/o) # phase shift
	#print(p)
	if p > 180:
		newP = 180 - p
	#print(newP)
	r = 0
	b = 0
	g = 0
	lower = 180
	mid = 270
	upper = 360
	if (p < lower and p >= 0): #If phase is betweek 144 and zero
		r = p / lower #R is highest
		g = (lower - p) / lower #G is lower
		b = 0 #B is zero
		#Yellow colour is produced
	elif (p >= lower and p <= mid): # If phase is between 144 and 288
		r = (mid - p) / lower # R is highest
		g = 0 # G is 0
		b = ((p - lower) / lower) # Blue is not zero
		#Purple colour is produced
	elif (p >= mid and p < upper): # If phase is between 288 and 360
		r = 0 # R is zero
		g = (p - mid) / 72
		b = (upper - p) / 72
		#Blue is highest, G is added
		#Cyan colour is produced
	print("	")

	R = math.floor(r * (mag))
	G = math.floor(g * (mag))
	B = math.floor(b * (mag))
	#B = B - 50
	bt = [R, G, B]
	nb = max(bt)
	if nb > 255:
		by = nb / 255
		R = R / by
		G = G / by
		B = B / by

	#Multiplied by magnitude for fade with distance than by 2 for brighter overall
	print(f"{R}, {G}, {B}, {p}")
	print("	")
	vi = getRgb(p)
	#Print all values in a row
	vt = [vi[0], vi[1], vi[2]]
	return vt

ledTiming(1, 2, 3)
