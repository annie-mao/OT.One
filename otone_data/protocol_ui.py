from baseProtocol import BaseProtocol

welcome = input("Welcome to the OT.One Protocol Editor.\n\
    Create a new protocol: 'N' \n\
    Edit existing protoco: 'E' \n\
    Quit: 'Q' \n\
    Please enter your choice: ")
if welcome == 'N':
    wait = True
    while wait:
        try:
            name = input("Protocol name: ")
            desc = input("Protocol description: ")
            notes = input("Protocol notes: ")
            wait = False
        except(SyntaxError,NameError):
            print("Invalid input. Please try again.")
    bp = BaseProtocol(name,desc,notes)

