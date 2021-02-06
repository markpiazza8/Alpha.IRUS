import serial

try:
    ser = serial.Serial('COM5', baudrate = 115200, timeout=1)
    print('\nConnected from Serial Port COM5\n')
except:
    print('\nConnect Exception\n')

#ser = serial.Serial('COM5', baudrate = 115200, timeout=1)