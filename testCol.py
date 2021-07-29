import cmath
import math

def ledTiming(xs, ys, ts):
	x = xs * 70
	y = ys * 70
	W = complex(x, y) # Define fourier operator with x and y input
	newP = 0

	mag = 0
	o = math.pi/180 # Degree symbol
	p = 0


	mag = abs(W) # get magnitude (increases as antenna gets closer to wire)
	p = 180 - ((cmath.phase(W))/o) # phase shift
	#print(p)
	if p > 180:
		newP = 180 - p
	#print(newP)
	r = 0
	b = 0
	g = 0
	lower = 144
	mid = 288
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
	print(r, g, b)

p = ledTiming(0, 1000, 1)
