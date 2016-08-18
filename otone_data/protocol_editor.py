from protocol_ui import ProtocolUI

UI = ProtocolUI()

inProgress = True
while inProgress:
    try:
        UI.welcome()
        
    except(SyntaxError,NameError) as err:
        print(err)

    except Exception as err:
        print(err)
