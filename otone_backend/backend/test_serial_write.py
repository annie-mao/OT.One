import serial
import time

# Must disable Linux connection to serial port for terminal
# use sudo raspi-config

ser = serial.Serial('/dev/ttyUSB0',baudrate=9600,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)
print(ser.isOpen())
ser.write('LID OPEN\r\n')
time.sleep(10)
ser.write('LID CLOSE\r\n')

ser.close
