from cycler import Cycler
import time

c = Cycler()
c.connect()
print("Serial open: {0}".format(c.portOpen))
#print(c.get_run('vesselType'))
#print(c.get_run('vesselVol'))
#c.set_calc()
#print(c.get_run('vesselType'))
#print(c.get_run('vesselVol'))
#resp=c.run_program('"TEST"')
#print(c.get_run('targetTemp'))
#print(c.get_run('blockTemp'))
#c.incubate(10,True)
#print(c.get_run('targetTemp'))
#print(c.get_run('blockTemp'))
#c.cancel()
#print(c.get_run())
#print(c.get_run('vesselType'))
#print(c.get_run('vesselVol'))
#for key,val in c._runQ.items():
#    print(key)
#    print(c.get_run(key))
#print("Canceling Run")
#c.cancel()
#while True:
#    resp = c.get_run()
#    print(resp)
#    if resp[0] == '""':
#        print("Run Ended")
#        break 
#    c.cancel()
#    time.sleep(1) 
#
print(c.lidOpen)
c.toggle_lid()
print(c.send(c._lid['status'])) 
print(c.lidOpen)
