
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

def pie(scr,color,center,radius,start_angle,stop_angle):
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
	time.sleep(0.1)

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

def ledTiming(x, y, ts):
	W = complex(1000, 1000) # Define fourier operator with x and y input
	newW = complex((x * -1), y)

	mag = 0
	o = math.pi/180 # Degree symbol
	p = 0


	mag = abs(W) # get magnitude (increases as antenna gets closer to wire)
	print("	")
	newP = 180 - ((cmath.phase(newW))/o)
	p = 180 - ((cmath.phase(W))/o) # phase shift
	thf(newP)
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
	print(nb)
	print(f"{R}, {G}, {B}")
	if nb > 255:
		by = nb / 255
		R = R / by
		G = G / by
		B = B / by

	#Multiplied by magnitude for fade with distance than by 2 for brighter overall
	print(f"{R}, {G}, {B}, {x}, {y}, {p}, {mag}")
	#Print all values in a row
	vt = [R, G, B]
	fileSet("colRec15.txt", R, G, B, ts)
	return vt # Return RGB array

def landDrone(cf):
	for i in range(30):
		cf.commander.send_position_setpoint(0, 0, 0.1, 0)
		time.sleep(0.1)
	cf.commander.send_stop_setpoint()

def setLed(cf, R, G, B):
	cf.param.set_value('ring.effect', '13')

	# Get LED memory and write to it
	mem = cf.mem.get_mems(MemoryElement.TYPE_DRIVER_LED)
	if len(mem) > 0:
		#mem[0].leds[0].set(r=R,   g=G, b=B)
		#mem[0].leds[1].set(r=R,   g=G, b=B)
		mem[0].leds[2].set(r=R,   g=G, b=B)
		mem[0].leds[3].set(r=R,   g=G, b=B)
		mem[0].leds[4].set(r=R,   g=G, b=B)
		"""mem[0].leds[5].set(r=R,   g=G, b=B)
		mem[0].leds[6].set(r=R,   g=G, b=B)
		mem[0].leds[7].set(r=R,   g=G, b=B)
		mem[0].leds[8].set(r=R,   g=G, b=B)
		mem[0].leds[9].set(r=R,   g=G, b=B)
		mem[0].leds[10].set(r=R,   g=G, b=B)
		mem[0].leds[11].set(r=R,   g=G, b=B)"""
		mem[0].write_data(None)

def setPose(cf, xCord, yCord):
	posi = (0, yCord, xCord, 0)
	cf.commander.send_position_setpoint(xCord, yCord, 0, 0)

def run_sequence(scf, sequence):
	cf = scf.cf
	try:
		#setPose(cf, 0, 0)
		time.sleep(1)
		while True:
			try:
				end = time.time()
				el = end - start
				afx = open("ardX.txt", "r")
				afy = open("ardY.txt", "r")
				ci = open("cycs.txt", "r")
				cic = ci.read()
				cycleN = int(ci)
				axC = afx.read()
				ayC = afy.read()
				amX = float(axC)
				amY = float(ayC)
				fx = open("coordX.txt", "r")
				fy = open("coordY.txt", "r")
				xC = fx.read()
				yC = fy.read()
				mX = 0.5 + (float(xC) / 3)
				mY = (float(yC))
				tm = time.time()
				print(cycleN)
				leT = ledTiming(amX, amY, tm)
				setLed(cf, leT[0], leT[1], leT[2])
				#realY = math.atan(yC / xC)
				fileSet("cordRec15.txt", mX, mY, el, tm)
				#setPose(cf, mX, mY)
			except Exception as e:
				print(e)
				if e == KeyboardInterrupt:
					print("   ")
					print("   ")
					print("Deads")
					print("   ")
					print("   ")
					print('Closing!')
					#landDrone()
					break

	except KeyboardInterrupt:

		print("   ")
		print("   ")
		print("Deads")
		print("   ")
		print("   ")
		print('Closing!')
		#landDrone()
	# Make sure that the last packet leaves before the link is closed
	# since the message queue is not flushed before closing


if __name__ == '__main__':
	cflib.crtp.init_drivers()

	with SyncCrazyflie(uri, cf=Crazyflie(rw_cache='./cache')) as scf:
		#reset_estimator(scf)
		# start_position_printing(scf)
		run_sequence(scf, sequence)
