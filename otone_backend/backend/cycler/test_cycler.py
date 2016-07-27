import Cycler

c = Cycler.Cycler()

resp=c.send(c._sys['block'])
print(resp)
resp=c.run_program('"TEST"')
print(resp)
#c.toggle_lid()
#print(c.ask(self._lid[status]))
