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
        'params':'HOTLID?\r\n',
        'temp':'LIDTEMP?\r\n', #current measured lid temp
        'changeSuccess':'LID PARAMETERS CHANGED\r\n',
        'tempErr':'INVALID LID TEMPERATURE\r\n',
        'offsetErr':'INVALID OFFSET\r\n',
        'modeErr':'INVALID MODE\r\n',
        'minErr':'INVALID MINIMUM\r\n'
    }

    _runQ={
        'targetTemp':'INCUBATE?\r\n',
        'params':'RUN?\r\n',
        'curStep':'STEP?\r\n',
        'stepNum':'SNUMBER?\r\n',
        'progTime':'PTIME?\r\n',
        'stepTime':'STIME?\r\n',
        'rampTime':'RTIME?\r\n',
        'holdTime':'HTIME?\r\n',
        'timeLeft':'ETIME?\r\n',
        'blockTemp':'BLOCKTEMP?\r\n',
        'calcTemp':'CALCTEMP?\r\n',
        'isPaused':'PAUSE?\r\n'
    }

    _runCmd={
        'nextStep':'PROCEED\r\n',
        'cancel':'CANCEL\r\n',
        'pause':'PAUSE\r\n',
        'resume':'RESUME\r\n'
    }

    _sys={
        'block':'BLOCK?\r\n',
        'blockCt':'BLOCKCOUNT?\r\n',
        'folders':'FOLDERS?\r\n',
        'progs':'PROGRAMS?\r\n'
    }

    progName = None
    # system defaults
    ctrl = 'CALC'
    lid = 'ON'
    lidMode = '"TRACKING"'
    lidOffset = 0
    lidMin = 20
    vesselType = "Tubes"
    vesselVol = 100

    def __init__(self,port='/dev/ttyUSB0'):
        """open serial connection
        Must disable Linux connection to serial port for terminal
        use sudo raspi-config
        confirm with rpi-serial-console status
        if not disabled, run sudo rpi-serial-console disable
        (script from github.com/lurch/rpi-serial-console
        """
        self.ser = serial.Serial(port,baudrate=9600,\
        bytesize=serial.EIGHTBITS,\
        parity=serial.PARITY_NONE,\
        stopbits=serial.STOPBITS_ONE)
        self.ser.timeout=1
#-------------------------- RAW DATA PROCESSING -------------------------
    def send(self,sendMsg):
        """send query to Cycler and return its response
        """
        resp=None
        self.ser.write(sendMsg)
        try:
            resp=self.ser.read(1000)
            if len(resp)>0:
                return resp
        except serial.SerialException:
            print("Serial error")

    def formatInput(self,strList):
        """format a list of strings into a single comma-delimited string
        to send to cycler
        """
        strOut=''
        for i in range(0,len(strList)):
            strOut += strList.pop(0)
            if strList:
                strOut += ','
            else:
                strOut += '\r\n'
                return strOut

    def formatOutput(self,rawStr):
        """format cycler output as a list of strings
        """
        return rawStr[:-2].split(',')
 
#--------------------------- GETTER/SETTERS ----------------------------
    def get_lid(self,query=None):
        """ get info about the state of the lid
        by default, return lid mode, offset/set temp, lid min"""
        if query:
            try:
                resp = self.send(self._lid[query])
                return resp
            except KeyError:
                print("Invalid lid query. Please try again.")
                return False
        else:
        #returns mode("TRACKING" or "CONSTANT"),offset(if "TRACKING") 
        #or set temp(if "CONSTANT"), and lid minimum
            lidParams=self.send(self._lid['params'])
            return lidParams[:-2].split(',') #remove \r\n

    def set_lid(self,mode,offsetOrTemp,lidMin):
        """change lid parameters. Returns True if success, False if error
        """
        lidParamsStr = self.formatInput(['HOTLID'+mode,offsetOrTemp,lidMin])
        resp = self.send(lidParamsStr)
        if resp == self._lid['changeSuccess']:
            return True
        elif resp == self._lid['tempErr'] or\
        resp == self._lid['offsetErr'] or\
        resp == self._lid['modeErr'] or\
        resp == self._lid['minErr']:
            print(resp)
            return False
 
    def get_run(self,query=None): 
        """ get info about the current program running
        """       
        if query:
            try:
                resp = self.send(self._runQ[query])
                return resp
            except KeyError:
                print('Invalid run query. Please try again.')
                return False
        else:
        #returns program name in "", cur control method, cur lid state
            runParams = self.send(self._runQ['params'])
            return self.formatOutput(runParams)
        
 
#----------------------------- COMMANDS --------------------------------
    def toggle_lid(self):
        """close lid if open, open if closed
        """
        lidStatus=self.send(self._lid['status'])
        if lidStatus == self._lid['isOpen']:
            self.send(self._lid['close'])
        elif lidStatus == self._lid['isClosed']:
            self.send(self._lid['open'])
       
    def run_program(self,progName,ctrl=None,lid=None):
        """run a named program in the cycler's files.
        specify control method BLOCK, PROBE, or CALC. CALC by default
        specify heated lid on or off. On by default
        """
        ctrl = ctrl or self.ctrl
        lid = lid or self.lid
        sendStr = self.formatInput(['RUN '+progName,ctrl,lid])
        self.send(sendStr)
    
    def cancel(self):
        """cancel the current running program
        """
        self.send(self._runCmd['cancel'])
