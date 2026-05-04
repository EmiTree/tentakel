import serial
import time
import keyboard
 
ser = serial.Serial(port='COM7', baudrate=115200, timeout=.01)
 
print("Starting up...")
time.sleep(2)
ser.write(b"Start\n")
 
servo_1_pos = 0
servo_2_pos = 0

def use_keys():
    global servo_1_pos, servo_2_pos

    if keyboard.is_pressed("w"):
        servo_1_pos = 180
    if keyboard.is_pressed("s"):
        servo_1_pos = 0
    if keyboard.is_pressed("a"):
        servo_2_pos = 180
    if keyboard.is_pressed("d"):
        servo_2_pos = 0
    if keyboard.is_pressed("z"):
        servo_2_pos = 90
    if keyboard.is_pressed("x"):
        servo_2_pos -= 1
    if keyboard.is_pressed("c"):
        servo_2_pos += 1
while True:
    use_keys()

    #print(ser.readline().decode("utf-8"))
    servo_1_command = f"A:{servo_1_pos}\n"
    ser.write(servo_1_command.encode("utf-8"))

    servo_2_command = f"B:{servo_2_pos}\n"
    ser.write(servo_2_command.encode("utf-8"))
    print(f"Sent commands: {servo_1_command}, {servo_2_command}")
    time.sleep(.1)    