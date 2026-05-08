print("Welkom bij de tentakel!")

# Importing libraries
import serial
import time
import matplotlib.pyplot as plt

# Importing other files
from pidcontrol import PIDController
from MotorConversion import MotorConverter
import config

def send_motor_commands(letter, pwm):
    dc_motor_command = f"{letter}:{int(pwm)}\n"
    ser.write(dc_motor_command.encode("utf-8"))

# Setting up serial communication
ser = serial.Serial(config.serial_port, config.baud_rate, timeout=config.serial_timeout) #(port, baudrate, timeout)
print("Starting up...")
time.sleep(config.startup_delay)
ser.write(config.start_command)

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

#-------------- Start plotting code------------------
#Storage for plotting
time_data = []
raw_angle_data = []
angle_data = []
pid_data = []
p_data = []
i_data = []
d_data = []
motor_output_data = []
pwm_a_data = []
pwm_b_data = []
#--------------End plotting code------------------continued in loop

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
            pwm_a_better = 60 + pwm_a / 100 * 50

            send_motor_commands("D", pwm_a_better)
            send_motor_commands("E", 0)
            send_motor_commands("F", pwm_a_better)
            send_motor_commands("G", 0)

        elif pwm_b > 0:
            #conversion to start at 50
            pwm_b_better = 60 + pwm_b / 100 * 50

            send_motor_commands("D", 0)
            send_motor_commands("E", pwm_b_better)
            send_motor_commands("F", 0)
            send_motor_commands("G", pwm_b_better)

        else:
            send_motor_commands("D", 0)
            send_motor_commands("E", 0)
            send_motor_commands("F", 0)
            send_motor_commands("G", 0)

        #-------------end motor actuation code---------------------

        #-------------Start plotting code in loop------------------
        #time for plotting, makes sure graph's starts at 0 seconds
        plot_time = current_time - start_time

        #Adding data for plotting to storage
        time_data.append(plot_time)
        raw_angle_data.append(raw_angle)
        angle_data.append(angle)
        pid_data.append(pid_output)
        p_data.append(p_value)
        i_data.append(i_value)
        d_data.append(d_value)
        motor_output_data.append(motor_output)
        pwm_a_data.append(pwm_a_better)
        pwm_b_data.append(pwm_b_better)
        #-------------End plotting code in loop------------------

    

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


print("Finished collecting data")

# Stop motors after run
send_motor_commands("D", 0)
send_motor_commands("E", 0)
send_motor_commands("F", 0)
send_motor_commands("G", 0)

#-------------- Start end graph code------------------

fig_end, axs_end = plt.subplots(4, 2, figsize=(14, 10))

# Angle data
axs_end[0, 0].plot(time_data, angle_data, color="blue", label="Angle")
axs_end[0, 0].axhline(config.setpoint, color="black", linewidth=1)
axs_end[0, 0].set_title("Angle")
axs_end[0, 0].set_ylabel("Angle")
axs_end[0, 0].set_ylim(config.angle_y_min, config.angle_y_max)

# PID output data
axs_end[0, 1].plot(time_data, pid_data, color="red", label="PID Output")
axs_end[0, 1].axhline(0, color="black", linewidth=1)
axs_end[0, 1].set_title("PID Output")
axs_end[0, 1].set_ylabel("PID Output")
axs_end[0, 1].set_ylim(config.pid_y_min, config.pid_y_max)

# P value
axs_end[1, 0].plot(time_data, p_data, color="green", label="P")
axs_end[1, 0].axhline(0, color="black", linewidth=1)
axs_end[1, 0].set_title("P Value")
axs_end[1, 0].set_ylabel("P")

# I value
axs_end[1, 1].plot(time_data, i_data, color="orange", label="I")
axs_end[1, 1].axhline(0, color="black", linewidth=1)
axs_end[1, 1].set_title("I Value")
axs_end[1, 1].set_ylabel("I")

# D value
axs_end[2, 0].plot(time_data, d_data, color="purple", label="D")
axs_end[2, 0].axhline(0, color="black", linewidth=1)
axs_end[2, 0].set_title("D Value")
axs_end[2, 0].set_ylabel("D")

# Motor output data
axs_end[2, 1].plot(time_data, motor_output_data, color="brown", label="Motor Output")
axs_end[2, 1].axhline(0, color="black", linewidth=1)
axs_end[2, 1].set_title("Motor Output")
axs_end[2, 1].set_ylabel("Motor Output")
axs_end[2, 1].set_ylim(config.motor_y_min, config.motor_y_max)

# PWM A
axs_end[3, 0].plot(time_data, pwm_a_data, color="cyan", label="PWM A")
axs_end[3, 0].set_title("PWM A")
axs_end[3, 0].set_ylabel("PWM A")
axs_end[3, 0].set_ylim(config.pwm_y_min, config.pwm_y_max)

# PWM B
axs_end[3, 1].plot(time_data, pwm_b_data, color="magenta", label="PWM B")
axs_end[3, 1].set_title("PWM B")
axs_end[3, 1].set_ylabel("PWM B")
axs_end[3, 1].set_ylim(config.pwm_y_min, config.pwm_y_max)

for ax in axs_end.flat:
    ax.set_xlabel("Time (s)")
    ax.set_xlim(0, run_time)
    ax.grid(True)
    ax.legend()

plt.tight_layout()
plt.show()

#-------------- End graph code------------------

