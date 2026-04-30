# %%
# Importing libraries
import numpy as np
import matplotlib.pyplot as plt


#Main variables for PID control
setpoint = 100  # Desired motor speed (RPM)
Kp = 0.1        # Proportional gain
Ki = 0.01       # Integral gain
Kd = 0.05       # Derivative gain
dt = 0.1        # Time step for simulation (seconds)
sim_time = 150   # Total simulation time (seconds)

#Initial values for PID control
integral = 0 # The integral term accumulates the error over time. We initialize it to 0.
previous_error = 0 # tracks the error from the previous time step to compute the derivative term.
motor_speed = 0  # Initial motor speed (RPM)

# Store data for plotting
time_data = []
speed_data = []
integral_data = []

#Main PID Loop
for t in np.arange(0, sim_time, dt):
    #Calculate error between setpoint and current motor speed
    error = setpoint - motor_speed

    # Proportional term
    P_out = Kp * error
        
    # Integral term (accumulation of past errors)
    integral += error * dt
    I_out = Ki * integral
        
    # Derivative term (rate of change of error)
    derivative = (error - previous_error) / dt
    D_out = Kd * derivative

    #Calculate the total control output
    control_output = P_out + I_out + D_out
        
    # Simulate the motor speed response (simplified linear response)
    motor_speed += control_output * dt

    # Update the previous error for the next iteration
    previous_error = error
        
    # Save data for plotting
    time_data.append(t)
    speed_data.append(motor_speed)
    integral_data.append(integral)  # Save the current integral value for plotting
    
# Plot motor speed and integral term next to each other
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left graph: motor speed
ax1.plot(time_data, speed_data, color='blue')
ax1.set_title('DC Motor Speed with PID Control')
ax1.set_xlabel('Time (s)')
ax1.set_ylabel('Speed (RPM)')
ax1.grid(True)

# Right graph: integral term
ax2.plot(time_data, integral_data, color='green')
ax2.set_title('Integral Term Over Time')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Integral Value')
ax2.grid(True)

# Makes sure labels/titles do not overlap
plt.tight_layout()

#dit plot 
plt.show()


# %%
