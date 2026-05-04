'''
This is code was used for testing and calibrating the wall
'''
 
 
 
import serial
import time
import keyboard

serial = serial.Serial(port='COM7', baudrate=115200, timeout=.01)
print("Starting up...")
time.sleep(2)
serial.write(b"Start\n")


def use_keys():
    global mode
    if keyboard.is_pressed('w'):
        #array[0] = 180
        for i in range(len(array)):
            array[i] = 180
 
    if keyboard.is_pressed('s'):
        #array[0] = 0
        for i in range(len(array)):
            array[i] = 0
 
    if keyboard.is_pressed('q'):
        array[a] = 180
 
    if keyboard.is_pressed('a'):
        array[a] = 0
   
while True:

    line = "A:180"
    serial.write(line.encode("ascii"))
    time.sleep()
    line = "A:0"
    serial.write(line.encode("ascii"))
    time.sleep(1)    