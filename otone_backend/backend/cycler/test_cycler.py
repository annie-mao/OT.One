import Cycler
import time

c = Cycler.Cycler()

resp=c.send(c._sys['block'])
print(resp)
resp=c.run_program('"TEST"')
print(c.get_run())
for key,val in c._runQ.items():
    print(key)
    print(c.get_run(key))
print("Canceling Run")
c.cancel()
while True:
    resp = c.get_run()
    print(resp)
    if resp[0] == '""':
        print("Run Ended")
        break
    c.cancel()
    time.sleep(1)
#c.toggle_lid()
#print(c.ask(self._lid[status]))
