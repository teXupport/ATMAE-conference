import socket

TCP_IP = '127.0.0.1'
TCP_PORT = 5010
BUFFER_SIZE = 1024
MESSAGE = "exit"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while 1:
    command = raw_input("Data: ")
    if (command == "w")         ## Forward
        MESSAGE = "LR"
    else if (command == "s")    ## Back
        MESSAGE = "lr"
    else if (command == "a")    ## Left
        MESSAGE = "lR"
    else if (command == "d")    ## Right
        MESSAGE = "Lr"
    else if (command == "t")    ## Autonomous Mode
        MESSAGE = "auto"
    else if (command == "g")    ## Conveyor
        MESSAGE = "c"
    else if (command == "b")    ## Brush
        MESSAGE = "b"
    else if (command == "y")    ## Swing Arm
        MESSAGE = "y"
    else if (command == "h")    ## PickUp Dustpan
        MESSAGE = "h"
    else if (command == "n")    ## Dump and Reset Dustpan
        MESSAGE = "n"
    else
        MESSAGE = "w"
    s.send(MESSAGE)
    if (MESSAGE == "exit"):
        break
    data = s.recv(BUFFER_SIZE)
    print "received data:", data

s.close()
