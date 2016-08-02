#!/usr/bin/env python3

"""
basic user command line for interacting with cycler
"""

from cycler import Cycler

c = Cycler()
c.connect()
c.ser.isOpen()
c.portOpen
while True:
    try:
        userIn = input("Input: ")
        if (userIn == 'q' or userIn == 'Q'):
            break
        else:
            print(c.send(userIn+'\r\n'))
    except(SyntaxError,NameError):
        print("Invalid input. Please try again or enter 'Q' to quit")

