from baseProtocol import BaseProtocol, InvalidEntry

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
    cmd = input("Add ingredient: 'I'\n\
        Add transfer: 'T'\n\
        Add mix: 'M'\n\
        Add cycler program: 'P'\n\
        Add cycler instruction: 'C'\n\
        Assign locations: 'A'\n\
        Export to JSON: 'J'\n\
        Quit: 'Q'\n\

        except InvalidEntry as err:
            print("Error: {0}".format(err.value))
    

