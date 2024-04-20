import serial
import os
from datetime import datetime
from mysql.connector import Error
import mysql.connector

serial = serial.Serial('/dev/ttyS0', 115200, timeout=1)

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')


try:
    db = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )
    cursor = db.cursor()

except Error as e:
    print(f"Error: {e}")
    exit(1)

while True:
    try:
        data = serial.readline().decode().strip()

        values = data.split(';')

        timestamp = datetime.now()
        time_str = timestamp.strftime('%H:%M:%S')

        insert_query = "INSERT INTO table_data (timestamp, time, temperature, pressure, humidity, latitude, longitude, height, velocity) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        data_tuple = (timestamp, time_str, *values)
        cursor.execute(insert_query, data_tuple)
        db.commit()
    except Exception as e:
        print(f"Error: {e}")

cursor.close()
db.close()
