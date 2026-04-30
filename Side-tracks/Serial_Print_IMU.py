import serial
import time

ser = serial.Serial('COM7', 115200, timeout=0.1)

print("ff wachten")
time.sleep(2)
ser.write(b"AAA\n")

while True:
    data = ser.readline().decode().strip()
    if data.startswith("S:"):
        yaw = float(data[2:])
        print(yaw)
    
    
