"""
basic user command line for interacting with cycler
"""

import Cycler

c = Cycler.Cycler()
while True:
    userIn = input("Input: ")
    # user inputs either Send:___ or Ask:___ or Q to quit
    if (userIn == 'q' or userIn == 'Q'):
        break
    else:
        print(c.send(userIn))
