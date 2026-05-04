# Serial settings
serial_port = 'COM7'
baud_rate = 115200
serial_timeout = 0.01
startup_delay = 2
start_command = b"Start\n"

# Initial variables kaas
calibration_coefficient = 0
kp = 1.0
ki = 0.1
kd = 0.1
setpoint = 0
max_pid_output = 200
max_pwm = 100
run_time = 20
live_points = 300

# Time commands for PID
min_dt = 0.01
print_interval = 0.1

# Plot settings
plot_interval = 0.1
figure_width = 12
figure_height = 5

angle_y_min = -180
angle_y_max = 180

pid_y_min = -300
pid_y_max = 300

motor_y_min = -100
motor_y_max = 100

pwm_y_min = 0
pwm_y_max = 100