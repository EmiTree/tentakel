import matplotlib.pyplot as plt
import time
import random

plt.ion()

fig, axs = plt.subplots(2, 2, figsize=(10, 7))

time_data = []
angle_data = []
pid_data = []
error_data = []
motor_data = []

angle_line, = axs[0, 0].plot([], [], color="blue")
pid_line, = axs[0, 1].plot([], [], color="red")
error_line, = axs[1, 0].plot([], [], color="green")
motor_line, = axs[1, 1].plot([], [], color="purple")

axs[0, 0].set_title("Angle")
axs[0, 1].set_title("PID Output")
axs[1, 0].set_title("Error")
axs[1, 1].set_title("Motor Command")

for ax in axs.flat: #sets x-label and grid for all subplots
    ax.set_xlabel("Time (s)")
    ax.grid(True)

start_time = time.time()

while True:
    t = time.time() - start_time

    angle = random.uniform(-30, 30)
    error = 0 - angle
    pid_output = error * 2
    motor_command = max(min(pid_output, 255), -255)

    time_data.append(t)
    angle_data.append(angle)
    pid_data.append(pid_output)
    error_data.append(error)
    motor_data.append(motor_command)

    angle_line.set_data(time_data, angle_data)
    pid_line.set_data(time_data, pid_data)
    error_line.set_data(time_data, error_data)
    motor_line.set_data(time_data, motor_data)

    for ax in axs.flat:
        ax.relim()
        ax.autoscale_view()

    plt.tight_layout()
    plt.pause(0.05)
