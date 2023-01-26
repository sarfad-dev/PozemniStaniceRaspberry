import serial
import time
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=5)
while True:
	print(ser.readline().decode('utf-8').rstrip())
	time.sleep(0.5)
