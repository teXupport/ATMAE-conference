import pygame, sys, math, random, time, socket, serial
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800,400))
TCP_IP = '192.168.1.106'
TCP_PORT = 5016
BUFFER_SIZE = 1024
MESSAGE = "w"
keyDown = 0
data = ""

##arduino = serial.Serial('/dev/ttyACM0',115200,timeout = .1)  # for Raspberry Pi
arduino = serial.Serial('COM4',115200,timeout = .1)  # for Windows computer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while 1:
    MESSAGE = "w"
    for event in pygame.event.get():
        
        if (((event.type == KEYDOWN) or event.type == KEYUP) and event.key == K_w and not keyDown):        ## Forward
            MESSAGE = "LR"
            if (not keyDown):
                    keyDown = 1
            else:
                    keyDown = 0
        elif (((event.type == KEYDOWN) or event.type == KEYUP) and event.key == K_s and not keyDown):   ## Back
            MESSAGE = "lr"
            if (not keyDown):
                    keyDown = 1
            else:
                    keyDown = 0
        elif (((event.type == KEYDOWN) or event.type == KEYUP) and event.key == K_a and not keyDown):    ## Left
            MESSAGE = "lR"
            if (not keyDown):
                    keyDown = 1
            else:
                    keyDown = 0
        elif (((event.type == KEYDOWN) or event.type == KEYUP) and event.key == K_d and not keyDown):   ## Right
            MESSAGE = "Lr"
            if (not keyDown):
                    keyDown = 1
            else:
                    keyDown = 0
        elif (event.type == KEYUP and event.key == K_t):   ## Autonomous Mode
            MESSAGE = "t"
        elif (event.type == KEYUP and event.key == K_g):  ## Conveyor
            MESSAGE = "c"
        elif (event.type == KEYUP and event.key == K_b):    ## Brush
            MESSAGE = "b"
        elif (event.type == KEYUP and event.key == K_y):   ## Swing Arm
            MESSAGE = "y"
        elif (event.type == KEYUP and event.key == K_h):  ## PickUp Dustpan
            MESSAGE = "h"
        elif (event.type == KEYUP and event.key == K_n):    ## Dump and Reset Dustpan
            MESSAGE = "n"
        elif (event.type == KEYUP and event.key == K_u):    ## Dump and Reset Dustpan
            flag = True
            MESSAGE = "u"
            s.send(MESSAGE.encode())
            while flag:
                    for event in pygame.event.get():
                            if (event.type == KEYUP and event.key == K_u):
                                    flag = False
                                    MESSAGE = "u"
                                    s.send(MESSAGE.encode())

                    if flag:
                        #read serial stuff
                        data = arduino.readline()
                        #send data: format(007127127127\n)
                      
                        if (data == "\n"):
                            continue
                        else:
                            s.send(data)
        elif (event.type == pygame.QUIT):
            MESSAGE = "k"
        else:
            MESSAGE = "w"
    
    if ((MESSAGE != "w") and (MESSAGE != "k")):
        print(MESSAGE)
        s.send(MESSAGE.encode())
    if (MESSAGE == "k"):
        s.send(MESSAGE.encode())
        pygame.quit()
        sys.exit()
        break

s.close()
