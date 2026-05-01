print("Welkom bij de tentakel!!!!")

# Importing libraries
import serial
import time
import matplotlib.pyplot as plt

# Importing other files
from pidcontrol import PIDController

# Setting up serial communication
ser = serial.Serial('COM7', 115200, timeout=0.5)
print("Starting up...")
time.sleep(2)
ser.write(b"Start\n")

# Initial variables
calibration_coefficient = 23.16
pid = PIDController(kp=1.0, ki=0.0, kd=0.1, setpoint=0)

# Time for PID
previous_time = time.time()

# Setting up live plot
plt.ion()

fig, axs = plt.subplots(1, 2, figsize=(12, 5))

time_data = []
angle_data = []
pid_data = []

start_time = time.time()
max_points = 1000

last_plot_time = time.time()
plot_interval = 0.05  # Update graph 20 times per second

last_print_time = time.time()
print_interval = 0.2  # Print 5 times per second

# Left graph: angle
angle_line, = axs[0].plot([], [], label="Angle", color="blue")
axs[0].axhline(0, color="black", linewidth=1)
axs[0].set_title("Live Angle")
axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("Angle")
axs[0].set_ylim(-180, 180)
axs[0].grid(True)
axs[0].legend()

# Right graph: PID output
pid_line, = axs[1].plot([], [], label="PID Output", color="red")
axs[1].axhline(0, color="black", linewidth=1)
axs[1].set_title("Live PID Output")
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("PID Output")
axs[1].set_ylim(-300, 300)
axs[1].grid(True)
axs[1].legend()

plt.tight_layout()

while True:
    data = ser.readline().decode().strip()

    if data.startswith("S:"):
        raw_angle = float(data[2:])
        angle = raw_angle + calibration_coefficient

        current_time = time.time()
        dt = current_time - previous_time
        previous_time = current_time

        pid_output, p_value, i_value, d_value = pid.update(
            setpoint=0,
            measured_value=angle,
            dt=dt
        )
        plot_time = current_time - start_time

        time_data.append(plot_time)
        angle_data.append(angle)
        pid_data.append(pid_output)

        time_data = time_data[-max_points:]
        angle_data = angle_data[-max_points:]
        pid_data = pid_data[-max_points:]

        now = time.time()

        if now - last_plot_time >= plot_interval:
            angle_line.set_data(time_data, angle_data)
            pid_line.set_data(time_data, pid_data)

            axs[0].set_xlim(max(0, plot_time - 10), plot_time)
            axs[1].set_xlim(max(0, plot_time - 10), plot_time)

            plt.pause(0.001)
            last_plot_time = now

        if now - last_print_time >= print_interval:
            print(
                f"Raw_angle: {raw_angle}, "
                f"Angle: {angle}, "
                f"PID Output: {pid_output}, "
                f"P: {p_value}, "
                f"I: {i_value}, "
                f"D: {d_value}"
            )   

        # Converting PID output to motor output
        # [WIP]
