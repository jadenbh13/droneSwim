import serial
import time
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
time.sleep(1) #give the connection a second to settle
file1 = "ardX.py"
file2 = "ardY.py"

while True:
	data = arduino.readline()
	if data and data !== "":
		bv = data.decode()
		spl = bv.split(",")
		with open(file1, 'w') as filetowrite:
			filetowrite.write(spl[0])
		with open(file2, 'w') as filetowrite:
			filetowrite.write(spl[1])
