import serial,json

ser = serial.Serial('/dev/ttyUSB0', 9600)

data = {}

while True:
    read_line = ser.readline().decode("utf-8").strip('\n').strip('\r')
    if read_line[-2:]== "16":
        pressure = float(read_line[:-3]) / 10
        data["pressure"] = pressure
    elif read_line[-2:]=="24":
        temperature = float(read_line[:-3]) / 10
        data["temperature"] = temperature
    elif read_line[-2:]=="32":
        humidity = float(read_line[:-3]) / 10
        data["humidity"] = humidity
    
    with open("data.json", "w") as outfile:
        json.dump(data, outfile)
    print(data)
