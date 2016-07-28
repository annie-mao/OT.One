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
        'temp':'LIDTEMP?\r\n' #current measured lid temp
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
        'folders':'FOLDERS?',
        'progs':'PROGRAMS?',
        'progInfo':'PROGRAM?'
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

    def formatInput(self,strList,delim):
        """format a list of strings into a single string
        to send to cycler. Delimiter specified by argument.
        """
        return (delim.join(strList)+'\r\n')

    def formatOutput(self,rawStr):
        """format cycler output as a list of strings
        """
        return rawStr[:-2].split(',')
 
#--------------------------- GETTER/SETTERS ----------------------------
#    def get_lid(self,query=None):
#        """ get info about the state of the lid
#        by default, return lid mode, offset/set temp, lid min"""
#        if query:
#            try:
#                resp = self.send(self._lid[query])
#                return resp
#            except KeyError:
#                print("Invalid lid query. Please try again.")
#                return False
#        else:
#        #returns mode("TRACKING" or "CONSTANT"),offset(if "TRACKING") 
#        #or set temp(if "CONSTANT"), and lid minimum
#            lidParams=self.send(self._lid['params'])
#            return lidParams[:-2].split(',') #remove \r\n
#
#    def set_lid(self,mode,offsetOrTemp,lidMin):
#        """change lid parameters. Returns True if success, False if error
#        """
#        lidParamsStr = self.formatInput(['HOTLID'+mode,offsetOrTemp,lidMin],',')
#        resp = self.send(lidParamsStr)
#        if resp == self._lid['changeSuccess']:
#            return True
#        elif resp == self._lid['tempErr'] or\
#        resp == self._lid['offsetErr'] or\
#        resp == self._lid['modeErr'] or\
#        resp == self._lid['minErr']:
#            print(resp)
#            return False
 
    def get_run(self,query=None): 
        """ get info about the current program running
        Returns info if successful, None if unsuccessful
        """       
        if query:
            try:
                resp = self.send(self._runQ[query])
            except KeyError:
                print('Invalid run query. Please try again.')
                return
        else:
        #returns program name in "", cur control method, cur lid state
            resp = self.formatOutput(self.send(self._runQ['params']))
        return resp
        

    def find_program(self,progName):
        """ checks if program exists on cycler.
        Returns True if yes, False if not
        """
        sendStr = self.formatInput([self._sys['progInfo'],progName],' ')
        if(self.send(sendStr)):
            return True
        else:
            return False

#----------------------------- COMMANDS --------------------------------
    def toggle_lid(self):
        """close lid if open, open if closed
        """
        lidStatus=self.send(self._lid['status'])
        if lidStatus == self._lid['isOpen']:
            self.send(self._lid['close'])
        elif lidStatus == self._lid['isClosed']:
            self.send(self._lid['open'])
       
    def is_lid_open(self):
        """Returns True if lid is open, False if closed
        """
        lidStatus=self.send(self._lid['status'])
        if lidStatus == self._lid['isOpen']:
            return True
        else:
            return False

    def run_program(self,progName,ctrl=None,lid=None):
        """run a named program in the cycler's files.
        specify control method BLOCK, PROBE, or CALC. CALC by default
        specify heated lid on or off. On by default
        Returns True if successful, False if not
        """
        # first check if program exists and exit program if not
        if not self.find_program(progName):
            print("Program does not exist")
            return False
        # make sure lid is closed
        if self.is_lid_open():
            self.toggle_lid()
        # control method is CALC by default, lid ON by default
        ctrl = ctrl or self.ctrl
        lid = lid or self.lid
        # send run command to cycler
        sendStr = self.formatInput(['RUN '+progName,ctrl,lid],',')
        self.send(sendStr)
        return True
    
    def cancel(self):
        """cancel the current running program
        check that RUN? returns an empty program name before returning
        """
        while True:
            if(self.get_run()[0]=='""'):
                break
            else:
                self.send(self._runCmd['cancel'])
                time.sleep(1)
