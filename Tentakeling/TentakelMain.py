print("Welkom bij de tentakel!!!!")

# Importing libraries
import serial
import time

#importing other files
from pidcontrol  import PIDController


# Setting up serial communication
ser = serial.Serial('COM7', 115200, timeout=0.1)
print("Starting up...")
time.sleep(2)
ser.write(b"Start\n")

#initial variables
calibration_coefficient = 23.16  # Placeholder for calibration coefficient
pid = PIDController(kp=1.0, ki=0.0, kd=0.1, setpoint=0)

#Working with time
previous_time = time.time() #gives current time in seconds, compare it later with new time

while True:
    data = ser.readline().decode().strip()
    
    if data.startswith("S:"):
        raw_angle = float(data[2:])  # remove "S:" and convert to number
        angle = raw_angle + calibration_coefficient  # apply calibration
        print(f"Angle: {angle}, Raw: {raw_angle}")
        
        current_time = time.time()
        dt = current_time - previous_time  # calculate time difference
        previous_time = current_time  # update previous time

        pid_output = pid.update(setpoint=0, measured_value=angle, dt=dt) 
        print(f"PID Output: {pid_output}")  
        
        #converting PID output to motor output
        #[WIP]