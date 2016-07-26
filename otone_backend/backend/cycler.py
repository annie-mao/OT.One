import serial
import time

class Cycler:
    
    # dictionaries of commands to send to cycler via serial port
    _lid={
        'status':'LID?\r\n',
        'open':'LID OPEN\r\n',
        'close':'LID CLOSE\r\n',
        'isOpen':'OPEN\r\n',
        'isClosed':'CLOSED\r\n',
        'isOpening':'OPENING\r\n',
        'isClosing':'CLOSING\r\n',
        'lidParams':'HOTLID?\r\n'
        'default':'ON'
    }

    _run={
        'targetTemp':'INCUBATE?\r\n',
        'curProg':'RUN?\r\n',
        'curStep':'STEP?\r\n',
        'stepNum':'SNUMBER?\r\n',
        'progTime':'PTIME?\r\n',
        'stepTime':'STIME?\r\n',
        'rampTime':'RTIME?\r\n',
        'holdTime':'HTIME?\r\n',
        'timeLeft':'ETIME?\r\n',
        'blockTemp':'BLOCKTEMP?\r\n',
        'calcTemp':'CALCTEMP?\r\n',
        'lidTemp':'LIDTEMP?\r\n',
        'nextStep':'PROCEED\r\n',
        'cancel':'CANCEL\r\n',
        'pause':'PAUSE\r\n',
        'isPaused':'PAUSE?\r\n'
        'resume':'RESUME\r\n'
    }

    _prog={
        'default':'CALC'    
    }

    def __init__(self,port='/dev/ttyUSB0'):
        """open serial connection
        Must disable Linux connection to serial port for terminal
        use sudo raspi-config
        """
        self.ser = serial.Serial(port,baudrate=9600,\
        bytesize=serial.EIGHTBITS,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE)
        self.ser.timeout=1

    def send(self,sendMsg):
        """send command to Cycler without waiting for response
        """
        self.ser.write(sendMsg)

    def ask(self,sendMsg):
        """send query to Cycler and return its response
        """
        self.ser.write(sendMsg)
        while True:
            try:
                resp=self.ser.read(1000)
                if len(resp)>0:
                    return resp
            except serial.SerialException:
                pass

    def toggle_lid(self):
        """close lid if open, open if closed
        """
        lidStatus=self.ask(self._lid['status'])
        if lidStatus == self._lid['isOpen']:
            self.send(self._lid['close'])
        elif lidStatus == self._lid['isClosed']:
            self.send(self._lid['open'])

    def run_program(self,progName,control=self._prog['default'],lid=self._lid['default']):
        sendStr = 'RUN "'+progName+'",'+control+','+lid+'\r\n'
        self.send(sendStr)



