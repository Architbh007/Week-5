import serial
import time
import firebase_admin
from firebase_admin import credentials, firestore
import json

# Set up serial communication (change COM5 to your Arduino port)
arduino_port = 'COM5'
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate)

# Firebase setup
cred = credentials.Certificate(r'C:\Users\Archit Bhullar\OneDrive\Documents\code\SI2255.1P\gyroscope-data-capture-firebase-adminsdk-6slb0-bcd12bd707.json')  
firebase_admin.initialize_app(cred)
db = firestore.client()

# Prepare to collect data
collection_duration = 30 * 60  # Collect data for 30 minutes (in seconds)
start_time = time.time()

print("Starting data collection and upload to Firebase...")

try:
    while time.time() - start_time < collection_duration:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()  # Read the serial data from Arduino

            # Check if the line contains three comma-separated values
            if line.count(',') == 2:
                try:
                    gx, gy, gz = map(float, line.split(','))  # Parse the values (x, y, z)
                    timestamp = time.time()

                    # Prepare the data in JSON format
                    data = {
                        'timestamp': timestamp,
                        'gx': gx,
                        'gy': gy,
                        'gz': gz
                    }

                    # Add the data to Firebase
                    db.collection('gyroscope_data').add(data)

                    print(f"Uploaded to Firebase: gx={gx}, gy={gy}, gz={gz}, timestamp={timestamp}")
                except ValueError:
                    print(f"Error parsing line: {line}")
            else:
                print(f"Invalid data format: {line}")

except KeyboardInterrupt:
    print("Data collection interrupted.")
finally:
    ser.close()
    print("Serial connection closed.")

