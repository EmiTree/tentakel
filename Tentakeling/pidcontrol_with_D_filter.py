class PIDController:
    def __init__(self, kp, ki, kd, setpoint=0, derivative_alpha=0.5):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.previous_error = 0
        self.integral = 0
        
        #Added for filtered derivative
        self.filtered_derivative = 0
        self.derivative_filter = derivative_alpha  # Adjust this value to change the filter strength, the higher the more the new derivative is taken with

    def update(self, setpoint, measured_value, dt):
        error = setpoint - measured_value

        self.integral += error * dt

        raw_derivative = (error - self.previous_error) / dt if dt > 0 else 0
        self.filtered_derivative = self.derivative_filter * raw_derivative + (1 - self.derivative_filter) * self.filtered_derivative

        p_value = self.kp * error
        i_value = self.ki * self.integral
        d_value = self.kd * self.filtered_derivative

        output = p_value + i_value + d_value

        self.previous_error = error

        return output, p_value, i_value, d_value
    
