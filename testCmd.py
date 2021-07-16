import pyvisa as visa
import numpy as np
from scipy.signal import butter, lfilter, freqz
import scipy
import math
import time
import matplotlib.animation as animation
import matplotlib.pyplot as plt

VISA_ADDRESS2 = 'USB0::10893::257::MY54500309::0::INSTR'
VISA_ADDRESS1 = 'USB0::10893::513::MY57700960::0::INSTR'
file1 = 'ardX.txt'
file2 = 'ardY.txt'

charList = [' ' , "'", 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbList = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-']

def onlyChars(st):
	nS = ""
	for t in st:
		if t in charList:
			nS += t
		else:
			kls = 0
	return nS

def onlyNumbs(st):
	nS = ""
	for t in st:
		if t in numbList:
			nS += t
		else:
			kls = 0
	return nS

def fileSet(name, one):
	with open(name, "a") as files:
		files.write(str(one))


def convertSci(inp):
	inpS = inp.lower()
	return float(inpS)

try:
	resourceManager = visa.ResourceManager()
	session1 = resourceManager.open_resource(VISA_ADDRESS1)
	session2 = resourceManager.open_resource(VISA_ADDRESS2)
	star = 0
	while True:
		#session1.write('*TRG')
		hu1 = session1.query('FETCh?')
		hu2 = session2.query('FETCh?')
		end = time.time()
		timeEl = end - star
		#print(1 / float(timeEl))
		try:
			r1 = convertSci(hu1)
			r2 = convertSci(hu2)
			print(f"Real: {r1}, Imaginary: {r2}")
			with open(file1, 'w') as filetowrite:
				filetowrite.write(str(r1))
			with open(file2, 'w') as filetowrite:
				filetowrite.write(str(r2))
		except Exception as e:
			print(e)
		session1.query('READ?')
		session2.query('READ?')
		star = end
	session1.close()
	session2.close()
	resourceManager.close()

except visa.Error as ex:
	print('An error occurred: %s' % ex)
	if ex == KeyboardInterrupt:
		print("   ")
		print("   ")
		print("Stopping")
		print("   ")
		print("   ")

print('Done.')
