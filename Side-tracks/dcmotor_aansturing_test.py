import serial
import time
import keyboard
 
ser = serial.Serial(port='COM7', baudrate=115200, timeout=.01)
 
print("Starting up...")
time.sleep(2)
ser.write(b"Start\n")
 
dc_motor_speed = 0

def use_keys():
    global dc_motor_speed

    if keyboard.is_pressed("b"):
        dc_motor_speed = 0
    if keyboard.is_pressed("n"):
        dc_motor_speed = 10
    if keyboard.is_pressed("m"):
        dc_motor_speed = 50
    if keyboard.is_pressed(","):
        dc_motor_speed = 100
    if keyboard.is_pressed("+"):
        dc_motor_speed -= 1
    if keyboard.is_pressed("-"):
        dc_motor_speed += 1
while True:
    use_keys()

    #print(ser.readline().decode("utf-8"))
    dc_motor_command = f"D:{dc_motor_speed}\n"
    ser.write(dc_motor_command.encode("utf-8"))

    print(f"Sent command: {dc_motor_command}")
    time.sleep(.1)   
