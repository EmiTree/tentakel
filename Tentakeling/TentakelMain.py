print("Welkom bij de tentakel!")

# Importing libraries
import serial
import time

# Setting up serial communication
ser = serial.Serial('COM7', 115200, timeout=0.1)
print("Starting up...")
time.sleep(2)
ser.write(b"Start\n")

#initial variables
calibration_coefficient = 23.16  # Placeholder for calibration coefficient


while True:
    data = ser.readline().decode().strip()
    
    if data.startswith("S:"):
        raw_angle = float(data[2:])  # remove "S:" and convert to number
        angle = raw_angle + calibration_coefficient  # apply calibration
        print(f"Angle: {angle}, Raw: {raw_angle}")
        
    