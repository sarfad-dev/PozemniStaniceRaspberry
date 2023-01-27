import serial
ser = serial.Serial('/dev/ttyACM0', 115200)
read_line = ser.readline().decode("utf-8").strip('\n').strip('\r')
if read_line > 1000000:
    print("pressure")
elif (read_line[-2:]==24):
    print("temperature")
elif (read_line[-2:]==32 and read_line<100000):
    print("humidity")   
