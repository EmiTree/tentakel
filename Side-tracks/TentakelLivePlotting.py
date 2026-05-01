print("Welkom bij de tentakel!!!!")

# Importing libraries
import serial
import time
import matplotlib.pyplot as plt

# Setting up serial communication
ser = serial.Serial('COM7', 115200, timeout=0.1)
print("Starting up...")
time.sleep(2)
ser.write(b"Start\n")

# Initial variables
calibration_coefficient = 0

# Setting up live plot
plt.ion()

fig, ax = plt.subplots()

time_data = []
angle_data = []

start_time = time.time()
max_points = 1000

last_plot_time = time.time()
plot_interval = 0.05  # Update graph 20 times per second

last_print_time = time.time()
print_interval = 0.2  # Print 5 times per second

angle_line, = ax.plot([], [], label="Angle")
ax.axhline(0, color="black", linewidth=1)

ax.set_title("Live Angle")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Angle")
ax.set_ylim(-180, 180)
ax.grid(True)
ax.legend()

while True:
    data = ser.readline().decode().strip()

    if data.startswith("S:"):
        raw_angle = float(data[2:])
        angle = raw_angle + calibration_coefficient

        current_time = time.time() - start_time

        time_data.append(current_time)
        angle_data.append(angle)

        time_data = time_data[-max_points:]
        angle_data = angle_data[-max_points:]

        now = time.time()

        if now - last_plot_time >= plot_interval:
            angle_line.set_data(time_data, angle_data)

            ax.set_xlim(max(0, current_time - 10), current_time)

            plt.pause(0.001)
            last_plot_time = now

        if now - last_print_time >= print_interval:
            print(f"Angle: {angle}, Raw: {raw_angle}")
            last_print_time = now
