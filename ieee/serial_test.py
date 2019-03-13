import serial
import numpy

ser = serial.Serial('/dev/ttyACM0',115200)
s = [0]

while True:
	try:
		data = ser.readline().rstrip()
		
		sensors = data.split('^')
		print(sensors)
		
	except ValueError:
		raise InputError('got bad value{}'.format(input))
		
	
	
