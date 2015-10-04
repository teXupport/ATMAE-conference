import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5010
BUFFER_SIZE = 1024
MESSAGE = "exit"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while 1:
    command = raw_input("Data: ")
    if (command == "w"):        ## Forward
        MESSAGE = "LR"
    elif (command == "s"):   ## Back
        MESSAGE = "lr"
    elif (command == "a"):    ## Left
        MESSAGE = "lR"
    elif (command == "d"):   ## Right
        MESSAGE = "Lr"
    elif (command == "t"):   ## Autonomous Mode
        MESSAGE = "auto"
    elif (command == "g"):  ## Conveyor
        MESSAGE = "c"
    elif (command == "b"):    ## Brush
        MESSAGE = "b"
    elif (command == "y"):   ## Swing Arm
        MESSAGE = "y"
    elif (command == "h"):  ## PickUp Dustpan
        MESSAGE = "h"
    elif (command == "n"):    ## Dump and Reset Dustpan
        MESSAGE = "n"
    elif ((command == "0") or (command == "1") or (command == "2") or (command == "3") or (command == "4") or (command == "5") or (command == "6") or (command == "7") or (command == "8") or (command == "9")):
        MESSAGE = command       # Motor voltage setting
    elif (command == "exit"):
        MESSAGE = "exit"
    elif (command == "kill"):
        MESSAGE = "kill"
    else:
        MESSAGE = "w"
    s.send(MESSAGE)
    if (MESSAGE == "exit" or MESSAGE == "kill"):
        break
    data = s.recv(BUFFER_SIZE)
    print "received data:", data

s.close()
