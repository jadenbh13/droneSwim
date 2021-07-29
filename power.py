
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
from simple_pid import PID
pid = PID(0.3, 0.05, 0.01, setpoint=0)

def getInp():
	afx = open("ardX.txt", "r")
	afy = open("ardY.txt", "r")
	axC = float(afx.read())
	ayC = float(afy.read())
	phs = math.atan(ayC / axC)
	return axC, ayC, phs
hb = getInp()
v = hb[2]
# URI to the Crazyflie to connect to
uri = uri_helper.uri_from_env(default='radio://0/80/2M/E7E7E7E7E7')

# Change the sequence according to your setup
#			 x	y	z  YAW
sequence = [
	(0, 0, 0.1, 0),
	(0, 0, 0.2, 0),
	(0, 0, 0.3, 0)
]
fileX = "coordX.txt"
fileY = "coordY.txt"

p = 0

start = time.time()
mn = 0
front = True
cycleN = 0
lasT = 100
prevNum = 0
xPos = 0
yPos = 0
rV = 0
gV = 0
bV = 0
BaseX = 0
BaseY = 0
boolAlt = True
mn = BaseX
basePhase = 0
"""def pie(scr,color,center,radius,start_angle,stop_angle):
	theta=start_angle
	while theta <= stop_angle:
		pygame.draw.line(scr,color,center,
		(center[0]+radius*cos(radians(theta)),center[1]-radius*sin(radians(theta))),2)
		theta+=0.01

def thf(ph):
	winWidth,winHeight=500,500
	bv = 0
	mt = random.randint(0, 360)
	scr=pygame.display.set_mode((winWidth,winHeight))
	pie(scr,(255,0,0),(winWidth//2,winHeight//2),250,0,ph)
	bv += 1
	pygame.display.update()
	time.sleep(0.1)"""

def wait_for_position_estimator(scf):
	print('Waiting for estimator to find position...')

	log_config = LogConfig(name='Kalman Variance', period_in_ms=500)
	log_config.add_variable('kalman.varPX', 'float')
	log_config.add_variable('kalman.varPY', 'float')
	log_config.add_variable('kalman.varPZ', 'float')

	var_y_history = [1000] * 10
	var_x_history = [1000] * 10
	var_z_history = [1000] * 10

	threshold = 0.001

	with SyncLogger(scf, log_config) as logger:
		for log_entry in logger:
			data = log_entry[1]

			var_x_history.append(data['kalman.varPX'])
			var_x_history.pop(0)
			var_y_history.append(data['kalman.varPY'])
			var_y_history.pop(0)
			var_z_history.append(data['kalman.varPZ'])
			var_z_history.pop(0)

			min_x = min(var_x_history)
			max_x = max(var_x_history)
			min_y = min(var_y_history)
			max_y = max(var_y_history)
			min_z = min(var_z_history)
			max_z = max(var_z_history)

			# print("{} {} {}".
			#	   format(max_x - min_x, max_y - min_y, max_z - min_z))

			if (max_x - min_x) < threshold and (
					max_y - min_y) < threshold and (
					max_z - min_z) < threshold:
				break


def reset_estimator(scf):
	cf = scf.cf
	cf.param.set_value('kalman.resetEstimation', '1')
	time.sleep(0.1)
	cf.param.set_value('kalman.resetEstimation', '0')

	wait_for_position_estimator(cf)


def position_callback(timestamp, data, logconf):
	x = data['kalman.stateX']
	y = data['kalman.stateY']
	z = data['kalman.stateZ']
	print('pos: ({}, {}, {})'.format(x, y, z))


def start_position_printing(scf):
	log_conf = LogConfig(name='Position', period_in_ms=500)
	log_conf.add_variable('kalman.stateX', 'float')
	log_conf.add_variable('kalman.stateY', 'float')
	log_conf.add_variable('kalman.stateZ', 'float')

	scf.cf.log.add_config(log_conf)
	log_conf.data_received_cb.add_callback(position_callback)
	log_conf.start()

def fileSet(name, one, two, three, ts):
	with open(name, "a") as files:
		files.write("\n")
		stV = str(one) + ", " + str(two) + ", " + str(three) + ", " + str(ts)
		files.write(stV)

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
		finalCol += [(jh / 255)]
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
				col1 = [255, 127.5, 0]
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
				col2 = [255, 127.5, 0]
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

magVal = 5
def ledTiming(xs, ys, ts):
	x = xs
	y = ys
	W = complex(x, y) # Define fourier operator with x and y input
	newP = 0

	mag = 0
	o = math.pi/180 # Degree symbol
	p = 0
	mgs = (abs(x) + abs(y)) / 2

	mag = abs(W) # get magnitude (increases as antenna gets closer to wire)
	p = (180 - ((cmath.phase(W))/o)) # phase shift
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
	print(mgs)
	vi = getRgb(p)
	#print([vi[0], vi[1], vi[2]])
	if mag > 0:
		R = math.floor(vi[0] * (mgs * magVal))
		G = math.floor(vi[1] * (mgs * magVal))
		B = math.floor(vi[2] * (mgs * magVal))
	else:
		R = 0
		G = 0
		B = 0
	#B = B - 50
	bt = [R, G, B]
	nb = max(bt)
	if nb > 255:
		by = nb / 255
		R = R / by
		G = G / by
		B = B / by

	#Multiplied by magnitude for fade with distance than by 2 for brighter overall
	#print(f"{R}, {G}, {B}, {p}")
	vt = [R, G, B]
	return vt

def setPose(cf, xCord, yCord):
	posi = (0, yCord, xCord, 0)
	cf.commander.send_position_setpoint(xCord, yCord, 1.1, 0)

def landDrone(cf):
	for i in range(30):
		cf.commander.send_position_setpoint(0.1, 0.1, 1.1, 0)
		time.sleep(0.1)
	for i in range(30):
		cf.commander.send_position_setpoint(0, 0, 0.5, 0)
		time.sleep(0.1)
	for i in range(30):
		cf.commander.send_position_setpoint(0, 0, 0.2, 0)
		time.sleep(0.1)
	for i in range(30):
		cf.commander.send_position_setpoint(0, 0, 0.1, 0)
		time.sleep(0.1)
	cf.commander.send_stop_setpoint()

def setLed(cf, R, G, B):
	cf.param.set_value('ring.effect', '13')

	# Get LED memory and write to it
	mem = cf.mem.get_mems(MemoryElement.TYPE_DRIVER_LED)
	if len(mem) > 0:
		if B < 200:
			mem[0].leds[2].set(r=R,   g=G, b=B)
			mem[0].leds[3].set(r=R,   g=G, b=B)
			mem[0].leds[4].set(r=R,   g=G, b=B)
			mem[0].write_data(None)
		else:
			mem[0].leds[2].set(r=R,   g=G, b=B)
			mem[0].leds[3].set(r=R,   g=G, b=B)
			mem[0].leds[4].set(r=R,   g=G, b=B)
			mem[0].write_data(None)

highNum = 0.9
def takeoff(cf):
	bv = 0
	time.sleep(30)
	while bv < highNum:
		setLed(cf, 0, 0, 0)
		print(bv)
		cf.commander.send_position_setpoint(0, 0, bv, 0)
		time.sleep(0.01)
		bv += 0.001
def land(cf):
	bv = highNum
	while bv > 0:
		setLed(cf, 0, 0, 0)
		print(bv)
		cf.commander.send_position_setpoint(0, 0, bv, 0)
		time.sleep(0.01)
		bv -= 0.001
	print("End")
	cf.commander.send_stop_setpoint()


def testSin3(cf, real, im, tm):
	#print(cycleN)
	global mn
	global front
	global cycleN
	W = complex(real, im)
	mag = abs(W) # get magnitude (increases as antenna gets closer to wire)
	phaseAngle = 180 - ((cmath.phase(W))/(math.pi/180))
	phase = 0
	amp = 3
	freq = 5
	sinWave = amp * math.sin((mn * freq) + math.radians(phase))
	addVal = 0.0003
	if mn > ((2 * math.pi) + 1):
		if front == True:
			cycleN += 1
			front = False
	if mn < 0:
		if front == False:
			cycleN += 1
			front = True
	if front == True:
		mn += addVal
	if front == False:
		mn -= addVal
	#time.sleep(0.01)
	return sinWave, mn

texFile = "powerText.txt"

def run_sequence(cf, sequence):
	cf = scf.cf
	global BaseX
	global BaseY
	global v
	global basePhase
	try:
		#takeoff(cf)
		basePhase = 50
		while True:
			try:
				end = time.time()
				el = end - start
				sinVal = math.sin(el)
				nj = getInp()
				amX = nj[0]
				amY = nj[1]
				si = testSin3(cf, amX, amY, el)
				mX = 0.5 + (si[0] / 10)
				mY = (si[1] / 10)
				tm = time.time()
				#print(control, math.degrees(phaseAng))
				desRan = 15
				W = complex(amX, amY)
				mag = abs(W) # get magnitude (increases as antenna gets closer to wire)
				phaseAngle = 180 - ((cmath.phase(W))/(math.pi/180))
				if phaseAngle > 180:
					phaseAngle = 180 - p
				#setPose(cf, mX, mY)
				i = 0
				red = 2
				"""while(i<3):
					angs = (abs(phaseAngle))
					if(phaseAngle>(basePhase + desRan)):
						out = abs(angs / 1000)
						mX += (out / red)
						print(phaseAngle)
						bo = getInp()
						amX = bo[0]
						amY = bo[1]
						#setPose(cf, mX, mY)
						#("Forward")
						W = complex(amX, amY)
						mag = abs(W) # get magnitude (increases as antenna gets closer to wire)
						phaseAngle = ((cmath.phase(W))/(math.pi/180))
						BaseY = mY
						time.sleep(0.0005)
					elif(phaseAngle<(basePhase - desRan)):
						out = abs(angs / 1000)
						mX -= (out / red)
						print(phaseAngle)
						bo = getInp()
						amX = bo[0]
						amY = bo[1]
						#setPose(cf, mX, mY)
						#print("Back")
						W = complex(amX, amY)
						mag = abs(W) # get magnitude (increases as antenna gets closer to wire)
						phaseAngle = ((cmath.phase(W))/(math.pi/180))
						BaseY = mY
						time.sleep(0.0005)
					else:
						print(phaseAngle)
						#setPose(cf, mX, BaseY)
						break
					i+=1
					#setPose(cf, mX, mY)"""
				bo = getInp()
				amX = bo[0]
				amY = bo[1]
				leT = ledTiming(amX, amY, 1)
				setLed(cf, leT[0], leT[1], leT[2])
				#fileSet(texFile, mX, mY, amX, amY)
				"""if cycleN == 1:
					print("   ")
					print("   ")
					print("Deads")
					print("   ")
					print("   ")
					print('Closing!')
					land(cf)
					fileSet(texFile, 0, 0, 0, 0)
					break"""
			except Exception as e:
				print(e)
				#setPose(cf, mX, BaseY)
				if e == KeyboardInterrupt:
					print("   ")
					print("   ")
					print("Deads")
					print("   ")
					print("   ")
					print('Closing!')
					#land(cf)
					break

	except KeyboardInterrupt:
		print("   ")
		print("   ")
		print("Deads")
		print("   ")
		print("   ")
		print('Closing!')
		#land(cf)
	# Make sure that the last packet leaves before the link is closed
	# since the message queue is not flushed before closing


if __name__ == '__main__':
	cflib.crtp.init_drivers()

	with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
		#reset_estimator(scf)
		# start_position_printing(scf)
		run_sequence(scf, sequence)
