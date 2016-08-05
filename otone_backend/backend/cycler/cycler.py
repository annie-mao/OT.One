import serial, time

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
        'lidTemp':'LIDTEMP?\r\n',
        'calcTemp':'CALCTEMP?\r\n',
        'isPaused':'PAUSE?\r\n',
        'vesselType':'VESSEL?\r\n',
        'vesselVol':'VOLUME?\r\n',
        'block':'BLOCK?\r\n'
    }

    _runCmd={
        'nextStep':'PROCEED\r\n',
        'cancel':'CANCEL\r\n',
        'pause':'PAUSE\r\n',
        'resume':'RESUME\r\n',
        'incubate':'INCUBATE'
    }

    _sys={
        'block':'BLOCK?\r\n',
        'folders':'FOLDERS?\r\n',
        'progs':'PROGRAMS?',
        'progInfo':'PROGRAM?',
        'vesselType':'VESSEL',
        'vesselVol':'VOLUME'
    }

    # system default settings
    progName = None
    ctrl = 'CALC'
    lid = 'ON'
    vesselType = '"Tubes"'
    vesselVol = 100

    # location on deck
    # restrict movement of pipette head to never cross these boundaries
    bounds = {
        'x':{'open':60,'closed':60},
        'y':{'open':270,'closed':270}
    }

    move_between = {
        'safe':[[1,1],[1,2],[2,1],[2,2],[2,3],[3,2],[3,3],[3,4],[4,3],[4,4],[4,5],[5,4],[5,5]],
        'collision':[[1,3],[3,1],[2,4],[4,2],[3,5],[5,3],[4,1],[1,4],[2,5],[5,2],[1,5],[5,1]],
        'check_lid':[[1,4],[2,4],[3,4]]
    }

    cell_nodes = {
        'open':{
            1:{'x':30,'y':135,'z':0},
            2:{'x':30,'y':330,'z':0},
            3:{'x':160,'y':330,'z':0},
            4:{'x':310,'y':330,'z':0},
            5:{'x':310,'y':135,'z':0}
        },
        'closed':{
            1:{'x':50,'y':135,'z':0},
            2:{'x':50,'y':330,'z':0},
            3:{'x':240,'y':330,'z':0}
        }
    }

    cell_bounds = {
        'open':{
            1:{'x':[0,60],'y':[0,270]},
            2:{'x':[0,60],'y':[270,390]},
            3:{'x':[60,260],'y':[270,390]},
            4:{'x':[260,382],'y':[270,390]},
            5:{'x':[260,382],'y':[0,270]}
        },
        'closed':{
            1:{'x':[0,100],'y':[0,270]},
            2:{'x':[0,100],'y':[270,390]},
            3:{'x':[100,382],'y':[270,390]},
            4:{'x':[100,382],'y':[0,270]}
        }
    }
   
    # state variables
    lidOpen = None
    portOpen = None

    def __init__(self):
        self.portOpen = self.connect()
    
    def connect(self,port='/dev/ttyUSB0'):
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

        self.lidOpen = self.is_lid_open()
        if self.lidOpen is not None:
            self.portOpen = True


#-------------------------- RAW DATA PROCESSING -------------------------
    def send(self,sendMsg):
        """send query to Cycler and return its response
        """
        resp=None
        self.ser.write(sendMsg.encode())
        try:
            resp=self.ser.read(1000)
            if len(resp)>0:
                return resp.decode()
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
        Name must be in quotes
        Returns True if yes, False if not
        """
        sendStr = self.formatInput([self._sys['progInfo'],progName],' ')
        if(self.send(sendStr)):
            return True
        else:
            return False

    def set_calc(self,vesselType=None,vesselVol=None):
        """ set the vessel type and volume used in the temperature
        calculation algorithm
        vesselType can be "Tubes" or "Plate" and vesseVol between 10-100
        "Tubes" and 100uL by default
        """
        vesselType = vesselType or self.vesselType
        vesselVol = vesselVol or self.vesselVol
        self.send(self.formatInput([self._sys['vesselType'],vesselType],' '))
        self.send(self.formatInput([self._sys['vesselVol'],str(vesselVol)],' '))


#----------------------------- COMMANDS --------------------------------
    def toggle_lid(self):
        """close lid if open, open if closed
        """
        if self.lidOpen == True:
            self.send(self._lid['close'])
            self.lidOpen = False
        elif self.lidOpen == False:
            self.send(self._lid['open'])
            self.lidOpen = True

    def is_lid_open(self):
        """Returns True if lid is open, False if closed
        """
        lidStatus=self.send(self._lid['status'])
        if lidStatus == self._lid['isOpen']:
            return True
        elif lidStatus == self._lid['isClosed']:
            return False
        else:
            return None

    def run_program(self,progName,ctrl=None,lid=None,vesselType=None,vesselVol=None):
        """run a named program in the cycler's files
        Name must be in quotes
        specify control method BLOCK, PROBE, or CALC. CALC by default
        specify heated lid on or off. On by default
        specify vessel type ('"Tubes"' or '"Plate"') and volume (10-100)
        Returns True if successful, False if not
        """
        # first check if program exists and exit program if not
        if not self.find_program(progName):
            print("Program does not exist")
            return False
        # make sure lid is closed
        if self.lidOpen:
            self.toggle_lid()
        # control method is CALC by default, lid ON by default
        ctrl = ctrl or self.ctrl
        lid = lid or self.lid
        # set temp calc algorithm parameters
        self.set_calc(vesselType,vesselVol)
        # send run command to cycler
        sendStr = self.formatInput(['RUN '+progName,ctrl,lid],',')
        self.send(sendStr)
        return True

    def incubate(self,temp,override=False):
        """activate current sample block and set to target temp(C)
        if override is set to True, the incubate command will override
        a currently running program. If override is False and a program
        is running, incubate() will exit and return False. If incubate
        is successful fn will return True
        """
        # if running another program, cancel
        if self.get_run()[0]:
            if override:
                self.cancel()
            else:
                return False
        sendStr = self.formatInput([self._runCmd['incubate'],str(temp)],' ')
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
