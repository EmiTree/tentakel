print("Welkom bij de tentakel!!!!")

import serial
import time
import matplotlib.pyplot as plt
from collections import deque

from pidcontrol import PIDController

ser = serial.Serial('COM7', 115200, timeout=0.01)
print("Starting up...")
time.sleep(2)
ser.write(b"Start\n")

calibration_coefficient = 23.16
pid = PIDController(kp=1.0, ki=1.0, kd=1.0, setpoint=0)

previous_time = time.time()
start_time = time.time()

max_points = 500

time_data = deque(maxlen=max_points)
angle_data = deque(maxlen=max_points)
pid_data = deque(maxlen=max_points)

plt.ion()

fig, axs = plt.subplots(1, 2, figsize=(12, 5))

angle_line, = axs[0].plot([], [], color="blue", label="Angle")
axs[0].axhline(0, color="black", linewidth=1)
axs[0].set_title("Live Angle")
axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("Angle")
axs[0].set_ylim(-180, 180)
axs[0].grid(True)
axs[0].legend()

pid_line, = axs[1].plot([], [], color="red", label="PID Output")
axs[1].axhline(0, color="black", linewidth=1)
axs[1].set_title("Live PID Output")
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("PID Output")
axs[1].set_ylim(-300, 300)
axs[1].grid(True)
axs[1].legend()

plt.tight_layout()
plt.show(block=False)

last_plot_time = time.time()
plot_interval = 0.1  # 10 graph updates per second

last_print_time = time.time()
print_interval = 0.1  # 10 prints per second

while True:
    data = ser.readline().decode(errors="ignore").strip()

    if not data:
        continue

    if data.startswith("S:"):
        raw_angle = float(data[2:])
        angle = raw_angle + calibration_coefficient

        current_time = time.time()
        dt = current_time - previous_time
        previous_time = current_time

        pid_output = pid.update(setpoint=0, measured_value=angle, dt=dt)

        plot_time = current_time - start_time

        time_data.append(plot_time)
        angle_data.append(angle)
        pid_data.append(pid_output)

        now = time.time()

        if now - last_plot_time >= plot_interval:
            angle_line.set_data(time_data, angle_data)
            pid_line.set_data(time_data, pid_data)

            x_min = max(0, plot_time - 10)
            x_max = max(10, plot_time)

            axs[0].set_xlim(x_min, x_max)
            axs[1].set_xlim(x_min, x_max)

            fig.canvas.draw_idle()
            fig.canvas.flush_events()

            last_plot_time = now

        if now - last_print_time >= print_interval:
            print(f"Raw_angle: {raw_angle}, Angle: {angle}, PID Output: {pid_output}, P: {pid.kp * error}, I: {pid.ki * pid.integral}, D: {pid.kd * derivative}")
            last_print_time = now
