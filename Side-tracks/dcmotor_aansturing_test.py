import serial
import time
import keyboard
 
ser = serial.Serial(port='COM7', baudrate=115200, timeout=.01)
 
print("Starting up...")
time.sleep(2)
ser.write(b"Start\n")
 
motor_1_pwm_1 = 0
motor_1_pwm_2 = 0

motor_2_pwm_1 = 0
motor_2_pwm_2 = 0

def send_motor_commands(letter, pwm):
    dc_motor_command = f"{letter}:{pwm}\n"
    ser.write(dc_motor_command.encode("utf-8"))

def use_keys():
    global motor_1_pwm_1, motor_1_pwm_2, motor_2_pwm_1, motor_2_pwm_2

    #rechterwiel vooruit
    if keyboard.is_pressed("1"):
        motor_1_pwm_1 += 10
    if keyboard.is_pressed("q"):
        motor_1_pwm_1 += 1
    if keyboard.is_pressed("a"):
        motor_1_pwm_1 -= 1
    if keyboard.is_pressed("z"):
        motor_1_pwm_1 -= 10
    
    #rechterwiel achteruit
    if keyboard.is_pressed("2"):
        motor_1_pwm_2 += 10
    if keyboard.is_pressed("w"):
        motor_1_pwm_2 += 1
    if keyboard.is_pressed("s"):
        motor_1_pwm_2 -= 1
    if keyboard.is_pressed("x"):
        motor_1_pwm_2 -= 10
    
    #linkerwiel vooruit
    if keyboard.is_pressed("3"):
        motor_2_pwm_1 += 10
    if keyboard.is_pressed("e"):
        motor_2_pwm_1 += 1
    if keyboard.is_pressed("d"):
        motor_2_pwm_1 -= 1
    if keyboard.is_pressed("c"):
        motor_2_pwm_1 -= 10
    
    #linkerwiel achteruit
    if keyboard.is_pressed("4"):
        motor_2_pwm_2 += 10
    if keyboard.is_pressed("r"):
        motor_2_pwm_2 += 1
    if keyboard.is_pressed("f"):
        motor_2_pwm_2 -= 1
    if keyboard.is_pressed("v"):
        motor_2_pwm_2 -= 10




    if keyboard.is_pressed("5"):
        motor_2_pwm_1 += 10
        motor_1_pwm_1 += 10
    if keyboard.is_pressed("t"):
        motor_2_pwm_1 += 1
        motor_1_pwm_1 += 1
    if keyboard.is_pressed("g"):
        motor_2_pwm_1 -= 1
        motor_1_pwm_1 -= 1
    if keyboard.is_pressed("b"):
        motor_2_pwm_1-= 10
        motor_1_pwm_1 -= 10
    if keyboard.is_pressed("6"):
        motor_2_pwm_2 += 10
        motor_1_pwm_2 += 10
    if keyboard.is_pressed("y"):
        motor_2_pwm_2 += 1
        motor_1_pwm_2 += 1
    if keyboard.is_pressed("h"):
        motor_2_pwm_2 -= 1
        motor_1_pwm_2 -= 1
    if keyboard.is_pressed("n"):
        motor_2_pwm_2-= 10
        motor_1_pwm_2 -= 10


    if keyboard.is_pressed("0"):
        motor_2_pwm_1 = motor_2_pwm_2 = motor_1_pwm_1 = motor_1_pwm_2 = 0

    
while True:
    use_keys()
    
    #conversion naar snelst bij 100 en stil bij 0:
    #motor_1_pwm_1 = 100 - motor_1_pwm_1
    #motor_1_pwm_2 = 100 - motor_1_pwm_2

    #print(ser.readline().decode("utf-8"))
    #rechterwiel vooruit
    dc_motor_command = f"D:{motor_1_pwm_1}\n"
    ser.write(dc_motor_command.encode("utf-8"))
    
    #rechterwiel achteruit
    dc_motor_command = f"E:{motor_1_pwm_2}\n"
    ser.write(dc_motor_command.encode("utf-8"))
    
    #linkerwiel vooruit
    dc_motor_command = f"F:{motor_2_pwm_1}\n"
    ser.write(dc_motor_command.encode("utf-8"))
    
    #linkerwiel achteruit
    dc_motor_command = f"G:{motor_2_pwm_2}\n"
    ser.write(dc_motor_command.encode("utf-8"))
    
    print(f"PWM1: {motor_1_pwm_1}, PWM2: {motor_1_pwm_2}, PWM3: {motor_2_pwm_1}, PWM4: {motor_2_pwm_2}")
    
    #print(f"Sent command: {dc_motor_command}")
    time.sleep(.1)   
