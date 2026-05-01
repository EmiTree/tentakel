class PIDController:
    def __init__(self, kp, ki, kd, setpoint=0):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.setpoint = setpoint
        self.previous_error = 0
        self.integral = 0

    def update(self, setpoint, measured_value, dt):
        error = setpoint - measured_value

        self.integral += error * dt

        derivative = (error - self.previous_error) / dt if dt > 0 else 0

        p_value = self.kp * error
        i_value = self.ki * self.integral
        d_value = self.kd * derivative

        output = p_value + i_value + d_value

        self.previous_error = error

        return output, p_value, i_value, d_value
    
