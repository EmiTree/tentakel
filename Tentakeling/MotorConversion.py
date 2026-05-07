class MotorConverter:
    def __init__(self, max_pid_output=10, max_pwm=100):
        self.max_pid_output = max_pid_output
        self.max_pwm = max_pwm

    def convert(self, pid_output):
        motor_output = pid_output / self.max_pid_output * self.max_pwm

        motor_output = max(-self.max_pwm, min(motor_output, self.max_pwm))

        if motor_output > 0:
            pwm_a = motor_output
            pwm_b = 0
        elif motor_output < 0:
            pwm_a = 0
            pwm_b = abs(motor_output)
        else:
            pwm_a = 0
            pwm_b = 0
        
        
        return pwm_a, pwm_b, motor_output
    
    
    
        
    
