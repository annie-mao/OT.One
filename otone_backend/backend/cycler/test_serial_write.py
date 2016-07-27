import serial
import time

# Must disable Linux connection to serial port for terminal
# use sudo raspi-config

ser = serial.Serial('/dev/ttyUSB0',baudrate=9600,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE)

waiting = True
resp = None
ser.timeout=1
ser.write('LID?\r\n')
while waiting:
    try:
        resp=ser.read(1000)
        if resp == 'OPEN\r\n':
            waiting=False
            ser.write('LID CLOSE\r\n')
        elif resp == 'CLOSED\r\n':
            waiting=False
            ser.write('LID OPEN\r\n')
    except serial.SerialException:
        pass
#ser.write('LID OPEN\r\n')
#time.sleep(10)
#ser.write('LID CLOSE\r\n')

ser.close
