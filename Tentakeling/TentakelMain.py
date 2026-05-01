print("Welkom bij de tentakel!")

# Importing libraries
import serial
import time
import matplotlib.pyplot as plt
from collections import deque

# Importing other files
from pidcontrol import PIDController

# Setting up serial communication
ser = serial.Serial('COM7', 115200, timeout=0.01) #(port, baudrate, timeout)
print("Starting up...")
time.sleep(2)
ser.write(b"Start\n")

# Initial variables
calibration_coefficient = 0 #changes the angle to match the real angle of the tentacle, is raw_angle + calibration_coefficient = angle
pid = PIDController(kp=1.0, ki=0.01, kd=0.0, setpoint=0)
run_time = 30 #how long the program should run, in seconds
start_time = time.time()
live_points = 300 #how many points are shown on the graph at the same time, more points can make the graph slower, but also smoother and more informative

# Time commands for PID
previous_time = time.time() #used for PID calculation
last_print_time = time.time() #used for terminal printing s
print_interval = 0.01  # controls how often the terminal prints the data, in seconds (0.1 means 10 prints per second)

#-------------- Start plotting code------------------
#Storage for plotting
time_data = []
raw_angle_data = []
angle_data = []
pid_data = []
p_data = []
i_data = []
d_data = []

# Setting up live plot
plt.ion()

# Setting up the figure and axes
fig, axs = plt.subplots(1, 2, figsize=(12, 5))

# Left graph: angle
angle_line, = axs[0].plot([], [], color="blue", label="Angle")
axs[0].axhline(0, color="black", linewidth=1)
axs[0].set_title("Angle")
axs[0].set_xlabel("Time (s)")
axs[0].set_ylabel("Angle")
axs[0].set_ylim(-180, 180)
axs[0].grid(True)
axs[0].legend()

# Right graph: PID output
pid_line, = axs[1].plot([], [], color="red", label="PID Output")
axs[1].axhline(0, color="black", linewidth=1)
axs[1].set_title("PID Output")
axs[1].set_xlabel("Time (s)")
axs[1].set_ylabel("PID Output")
axs[1].set_ylim(-300, 300)
axs[1].grid(True)
axs[1].legend()

# Adjust layout and show the plot
plt.tight_layout() #lay-out of the graphs, so they don't overlap
plt.show(block=False) #open the plot window, but do not pause the Python program there.

#interval settings for plotting and printing
last_plot_time = time.time()
plot_interval = 0.2  # Update graph 5 times per second

last_print_time = time.time()
print_interval = 0.2  # Print 5 times per second

#--------------End plotting code------------------continued in loop

while time.time() - start_time < run_time:
    #reads bytes and turns bytes into text
    data = ser.readline().decode(errors="ignore").strip() 

    #failsafe if no data is received, skips the rest of the loop and starts a new one
    if not data:
        plt.pause(0.001)
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

        #-------------Start plotting code in loop------------------
        #time for plotting, makes sure graph's starts at 0 seconds
        plot_time = current_time - start_time
        now = time.time()

        #Adding data for plotting to storage
        time_data.append(plot_time)
        raw_angle_data.append(raw_angle)
        angle_data.append(angle)
        pid_data.append(pid_output)
        p_data.append(p_value)
        i_data.append(i_value)
        d_data.append(d_value)
        
        #Updating live graph without making program too slow, based on the plot_interval
        if now - last_plot_time >= plot_interval: #checks if enough time has passed since the last plot, based on the plot_interval
            angle_line.set_data(time_data, angle_data) #updates graph
            pid_line.set_data(time_data, pid_data) #updates graph

            axs[0].set_xlim(0, run_time)
            axs[1].set_xlim(0, run_time)

            #For extra smoothness
            fig.canvas.draw_idle()  #Redraw the figure when you get a chance.
            fig.canvas.flush_events() #Process the graph window events now.


            last_plot_time = now
        
        #-------------End plotting code in loop------------------
        
        now = time.time()

        if now - last_print_time >= print_interval: #checks if enough time has passed since the last print, based on the print_interval
            print(
                f"Raw_angle: {raw_angle:.2f}, "
                f"Angle: {angle:.2f}, "
                f"PID Output: {pid_output:.2f}, "
                f"P: {p_value:.2f}, "
                f"I: {i_value:.2f}, "
                f"D: {d_value:.2f}"
            )
            last_print_time = now #updates the last_print_time to the current time after printing, so the next print will wait for the print_interval again


print("Finished collecting data")

angle_line.set_data(time_data, angle_data)
pid_line.set_data(time_data, pid_data)

axs[0].set_xlim(0, run_time)
axs[1].set_xlim(0, run_time)

fig.canvas.draw_idle()
fig.canvas.flush_events()

plt.ioff()
plt.show()
