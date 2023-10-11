import serial
import time

ser = serial.Serial('COM5',9600)

while 1000:
    val = input('Enter 1,2,3,4: ')
    ser.write(val.encode())