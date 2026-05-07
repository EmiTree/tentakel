print("Welkom bij de tentakel!")

# Importing libraries
import serial
import time

# Importing other files
from pidcontrol import PIDController
from MotorConversion import MotorConverter
import config

# Setting up serial communication
ser = serial.Serial(config.serial_port, config.baud_rate, timeout=config.serial_timeout) #(port, baudrate, timeout)
print("Starting up...")
time.sleep(config.startup_delay)
ser.write(config.start_command)

def send_motor_commands(letter, pwm):
    dc_motor_command = f"{letter}:{int(pwm)}\n"
    ser.write(dc_motor_command.encode("utf-8"))

# Initial variables
calibration_coefficient = config.calibration_coefficient #changes the angle to match the real angle of the tentacle, is raw_angle + calibration_coefficient = angle
pid = PIDController(kp=config.kp, ki=config.ki, kd=config.kd, setpoint=config.setpoint)
motor_converter = MotorConverter(max_pid_output=config.max_pid_output, max_pwm=config.max_pwm)
run_time = config.run_time #how long the program should run, in seconds
start_time = time.time()

# Time commands for PID
previous_time = time.time() #used for PID calculation
last_print_time = time.time() #used for terminal printing s
print_interval = config.print_interval  # controls how often the terminal prints the data, in seconds (0.1 means 10 prints per second)

while time.time() - start_time < run_time:
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

        if dt < config.min_dt:
            dt = config.min_dt

        pid_output, p_value, i_value, d_value = pid.update(
            setpoint=config.setpoint,
            measured_value=angle,
            dt=dt
        )

        # Convert PID output to motor commands
        pwm_a, pwm_b, motor_output = motor_converter.convert(pid_output)

        #-------------Start motor actuation code------------------

        if pwm_a > 0:
            #conversion to start at 50
            pwm_a_better = 55 + pwm_a/100*50
            pwm_b_better = 55 + pwm_b/100*50
            
            send_motor_commands("D", pwm_a_better)
            send_motor_commands("E", 0)
            send_motor_commands("F", pwm_a_better)
            send_motor_commands("G", 0)
        else:
            #conversion to start at 50
            pwm_a_better = 50 + pwm_a/100*50
            pwm_b_better = 50 + pwm_b/100*50
            
            send_motor_commands("D", 0)
            send_motor_commands("E", pwm_b_better)
            send_motor_commands("F", 0)
            send_motor_commands("G", pwm_b_better)

        #-------------end motor actuation code---------------------

        now = time.time()

        #checks if enough time has passed since the last print, based on the print_interval
        if now - last_print_time >= print_interval:
            print(
                #f"Raw_angle: {raw_angle:.2f}, "
                f"Angle: {angle:.2f}, "
                f"PID Output: {pid_output:.2f}, "
                f"P: {p_value:.2f}, "
                f"I: {i_value:.2f}, "
                f"D: {d_value:.2f}, "
                f"Motor Output: {motor_output:.2f}, "
                f"PWM A: {pwm_a:.2f}, "
                f"PWM B: {pwm_b:.2f}, "
                f"dt: {dt:.3f}s"
            )
            last_print_time = now #updates the last_print_time to the current time after printing, so the next print will wait for the print_interval again

print("Finished running")
