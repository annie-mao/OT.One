import serial, time, sys
sys.path.append("..")
from file_io import FileIO

debug = True

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
    lid = 'OFF'
    vesselType = '"Tubes"'
    vesselVol = 100

    # location on deck
    # restrict movement of pipette head to never cross these boundaries

    move_between = {
        'safe':[[1,1],[1,2],[2,1],[2,2],[2,3],[3,2],[3,3],[3,4],[4,3],[4,4],[4,5],[5,4],[5,5],[2,4],[4,2]],
        'collision':[[1,3],[3,1],[3,5],[5,3],[4,1],[1,4],[2,5],[5,2],[1,5],[5,1]],
        'check_lid':[[1,5],[2,5],[3,5],[4,5]]
    }

    home = {
        'x': {
            'safe':[1,2,3,4],
            'target':{1:1,2:2,3:2,4:2}
        },
        'y': {
            'safe':[1,2,5],
            'target':{1:1,2:1,5:5}
        }
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
            3:{'x':180,'y':330,'z':0},
            4:{'x':310,'y':330,'z':0},
            5:{'x':310,'y':135,'z':0}
        }
    }

    cell_bounds = {
        'open':{
            1:{'x':[0,60],'y':[0,250]},
            2:{'x':[0,60],'y':[250,390]},
            3:{'x':[60,260],'y':[250,390]},
            4:{'x':[260,382],'y':[250,390]},
            5:{'x':[260,382],'y':[0,250]}
        },
        'closed':{
            1:{'x':[0,135],'y':[0,250]},
            2:{'x':[0,135],'y':[250,390]},
            3:{'x':[135,260],'y':[250,390]},
            4:{'x':[260,382],'y':[250,390]},
            5:{'x':[260,382],'y':[0,250]}
        }
    }
   
    # state variables
    lidOpen = None
    portOpen = None
    is_busy = False

    def __init__(self,head=None):
        self.portOpen = self.connect()
        self.head = head
        if debug == True: FileIO.log("Cycler init")
    
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

        if self.is_lid_open() is not None:
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

    def format_input(self,strList,delim):
        """format a list of strings into a single string
        to send to cycler. Delimiter specified by argument.
        """
        return (delim.join(strList)+'\r\n')

    def format_output(self,rawStr):
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
                resp = self.format_output(self.send(self._runQ[query]))
            except KeyError:
                print('Invalid run query. Please try again.')
                return
        else:
        #returns program name in "", cur control method, cur lid state
            resp = self.format_output(self.send(self._runQ['params']))
        return resp
        

    def find_program(self,progName):
        """ checks if program exists on cycler.
        Name must be in quotes
        Returns True if yes, False if not
        """
        sendStr = self.format_input([self._sys['progInfo'],progName],' ')
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
        self.send(self.format_input([self._sys['vesselType'],vesselType],' '))
        self.send(self.format_input([self._sys['vesselVol'],str(vesselVol)],' '))

    def check_busy(self):
        """ returns True if a program is currently running, False if otherwise
        """
        try:
            sn = self.get_run('stepNum')
            FileIO.log('step num resp: {0}'.format(sn))
            sn = sn[0]
            if sn == '0':
                FileIO.log('checked {0} is 0'.format(sn))
                self.is_busy = False
            else:
                FileIO.log('checked {0} not 0'.format(sn))
                self.is_busy = True
            return self.is_busy
        except TypeError as ex:
            FileIO.log('Cycler.check_busy error {0} args {1!r}\n'.format(type(ex).__name__,ex.args))
            self.is_busy = True
            return self.is_busy

#------------------------------ HELPERS---------------------------------

    def cell(self,x,y):
        """ Returns cell of x,y location relative to cycler
        lid closed          lid open
        0-------------x     0-------------x
        |1     |6|5   |     |1  |6//|5    |
        |      |/|cyc |     |lid|///|cycl.|
        |-------------|     |-------------|
        |2     |3|4   |     |2  |3  |4    |
        |      | |    |     |   |   |     |
        y-------------.     y-------------.
        """
        
        if self.lidOpen:
            lid = 'open'
        else:
            lid = 'closed'
        bounds = self.cell_bounds[lid]

        for cell,coords in bounds.items():
            if(x >= coords['x'][0] and x < coords['x'][1] and \
                y >= coords['y'][0] and y < coords['y'][1]):
                return cell
        #if no matches
        return None

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
            self.lidOpen = True
            return True
        elif lidStatus == self._lid['isClosed']:
            self.lidOpen = False
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
        # cancel other programs
        if self.check_busy():
            self.cancel()
        # make sure lid is closed
        if self.lidOpen:
            self.toggle_lid()
        # control method is CALC by default, lid ON by default
        ctrl = ctrl or self.ctrl
        lid = lid or self.lid
        # set temp calc algorithm parameters
        self.set_calc(vesselType,vesselVol)
        # send run command to cycler
        sendStr = self.format_input(['RUN '+progName,ctrl,lid],',')
        if debug == True: FileIO.log('cycler.py sending {0}'.format(sendStr))
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
        if self.get_run()[0]!='""':
            if override:
                self.cancel()
            else:
                return False
        sendStr = self.format_input([self._runCmd['incubate'],str(temp)],' ')
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


    def task(self,data):
        """handle incoming task from the_queue.py
        data = {
            'command': 'cycler',
            'name': 'PFunkel_1'
            'runtime': 7,
            'control': 'CALC',
            'heatedlid': True,
            'vessel': 'Tubes',
            'volume': 100
        }
        data = {
            'command': 'cycler',
            'lid': True 
        }

        """
        if debug == True: FileIO.log('CYCLER RECEIVED TASK:\n{0}'.format(data))
        name = data.get('name')
        if(name):
            self.head.theQueue.pause_job()
            self.is_busy = True
            # parse input
            name = '"' + name + '"'
            ctrl = data.get('control')
            heatedLid = data.get('heated-lid')
            if heatedLid:
                heatedLid = 'ON'
            else:
                heatedLid = 'OFF'
            vesselType = data.get('vessel')
            if vesselType:
                vesselType = '"'+data.get('vessel')+'"'
            vesselVol = data.get('volume')
            runSuccess = self.run_program(name,ctrl,heatedLid,vesselType,vesselVol)
            if not runSuccess and debug == True: FileIO.log('CYCLER RUN ERROR')
            elif debug == True: FileIO.log('CYCLER RUN SUCCESS')
            # wait for task to finish
            while self.check_busy():
                FileIO.log('cycler.py Still busy')
            # if program has a hold step, incubate at the hold temperature
            if debug == True: FileIO.log('cycler.py exit while')
            holdTemp = data.get('hold')
            if debug == True: FileIO.log('hold temp {0}'.format(holdTemp))
            if holdTemp:
                incSuccess = self.incubate(holdTemp,True)
                if not incSuccess and debug == True: FileIO.log('CYCLER INCUBATE ERROR')
                elif debug == True: FileIO.log('CYCLER HOLD AT {0} C'.format(holdTemp))
            self.head.theQueue.resume_job()
            self.head.smoothieAPI.delay(1)
        elif('lid' in data):
            if (data.get('lid') == True and self.lidOpen) or (data.get('lid') == False and not self.lidOpen):
                self.toggle_lid()
            


