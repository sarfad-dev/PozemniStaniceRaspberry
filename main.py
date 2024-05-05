import os
from datetime import datetime, timedelta
from mysql.connector import Error
import mysql.connector
from dotenv import load_dotenv
import serial
import serial.tools.list_ports
from colorama import init, Fore, Style

init()
load_dotenv()

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

print(f"{Fore.GREEN}Available serial ports:{Style.RESET_ALL}")
ports = list(serial.tools.list_ports.comports())
for i, port in enumerate(ports):
    print(f"{Fore.CYAN}{i}: {port.device} - {port.description}{Style.RESET_ALL}")

port_number = int(input(f"{Fore.YELLOW}Enter the number of the port your Arduino is connected to: {Style.RESET_ALL}"))

if port_number < 0 or port_number >= len(ports):
    print(f"{Fore.RED}Invalid port number. Exiting.{Style.RESET_ALL}")
    exit(1)

port_device = ports[port_number].device

try:
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = db.cursor()
except Error as e:
    print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
    exit(1)

arduino_serial = serial.Serial(port_device, 9600)

last_inserted_second = None

while True:
    try:
        data = arduino_serial.readline().decode().strip()

        values = data.split(';')

        serial_time = datetime.strptime(values[0], '%H:%M:%S') + timedelta(hours=2)
        time_str = serial_time.strftime('%H:%M:%S')
        current_second = serial_time.second

        if current_second != last_inserted_second:
            timestamp = datetime.now()
            insert_query = "INSERT INTO sarfad_data (timestamp, time, temperature, pressure, humidity, latitude, longitude, height, velocity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            
            data_tuple = (timestamp, time_str, *values[1:])
            print(data_tuple)

            cursor.execute(insert_query, data_tuple)
            db.commit()

            last_inserted_second = current_second
    except Exception as e:
        print(f"Error: {e}")

cursor.close()
db.close()
