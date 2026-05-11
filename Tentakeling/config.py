# Serial settings
serial_port = 'COM7'
baud_rate = 115200
serial_timeout = 0.01
startup_delay = 2
start_command = b"Start\n"

# Initial variables
calibration_coefficient = 0
kp = 5
ki = 0.01
kd = 0.5
setpoint = 0
max_pid_output = 140
max_pwm = 100
run_time = 10
add_on_pwm = 70
live_points = 300

# Derivative filter settings
derivative_alpha = 0.5  # Adjust this value to change the filter strength, the higher the more the new derivative is taken with

# Time commands for PID
min_dt = 0.01
print_interval = 0.1

# Plot settings (not needed anymore)
plot_interval = 0.1
figure_width = 12
figure_height = 5

angle_y_min = -180
angle_y_max = 180

pid_y_min = -100
pid_y_max = 100

motor_y_min = -100
motor_y_max = 100   

pwm_y_min = 0       
pwm_y_max = 100