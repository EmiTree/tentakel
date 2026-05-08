print("Welkom bij de tentakel!")

# Importing libraries
import serial
import time

# Importing other files
from BacklogTentakel.b_pidcontrol import PIDController

# Setting up serial communication
ser = serial.Serial('COM7', 115200, timeout=0.01) #(port, baudrate, timeout)
print("Starting up...")
time.sleep(2)
ser.write(b"Start\n")

# Initial variables
calibration_coefficient = 0 #changes the angle to match the real angle of the tentacle, is raw_angle + calibration_coefficient = angle
pid = PIDController(kp=1.0, ki=1.0, kd=1.0, setpoint=0)

# Time commands for PID
previous_time = time.time() #used for PID calculation
last_print_time = time.time() #used for terminal printing s
print_interval = 0.1  # controls how often the terminal prints the data, in seconds (0.1 means 10 prints per second)


while True:
    #reads bytes and turns bytes into text
    data = ser.readline().decode(errors="ignore").strip() 

    #failsafe if no data is received, skips the rest of the loop and starts a new one
    if not data:
        continue
    
    #Data starts with "S:" when it's an angle reading, so we check for that
    if data.startswith("S:"):
        raw_angle = float(data[2:]) #turns the text after "S:" into a number, this is the raw angle from the IMU
        angle = raw_angle + calibration_coefficient 

        current_time = time.time()
        dt = current_time - previous_time
        previous_time = current_time #updates the previous_time to the current time for the next loop

        pid_output, p_value, i_value, d_value = pid.update(
            setpoint=0,
            measured_value=angle,
            dt=dt
        )

        now = time.time()

        if now - last_print_time >= print_interval: #checks if enough time has passed since the last print, based on the print_interval
            print(
                f"Raw_angle: {raw_angle:.2f}, "
                f"Angle: {angle:.2f}, "
                f"PID Output: {pid_output:.2f}, "
                f"P: {p_value:.2f}, "
                f"I: {i_value:.2f}, "
                f"D: {d_value:.2f}"
                f" (dt: {dt:.3f}s)"
            )
            last_print_time = now #updates the last_print_time to the current time after printing, so the next print will wait for the print_interval again
