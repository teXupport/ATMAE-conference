import pygame, sys, math, random, socket
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800,400))
TCP_IP = '127.0.0.1'
TCP_PORT = 5018
BUFFER_SIZE = 1024
MESSAGE = "w"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while 1:
    MESSAGE = "w"
    for event in pygame.event.get():
        
        if (((event.type == KEYDOWN) or event.type == KEYUP) and event.key == K_w):        ## Forward
            MESSAGE = "LR"
        elif (((event.type == KEYDOWN) or event.type == KEYUP) and event.key == K_s):   ## Back
            MESSAGE = "lr"
        elif (((event.type == KEYDOWN) or event.type == KEYUP) and event.key == K_a):    ## Left
            MESSAGE = "lR"
        elif (((event.type == KEYDOWN) or event.type == KEYUP) and event.key == K_d):   ## Right
            MESSAGE = "Lr"
        elif (event.type == KEYUP and event.key == K_t):   ## Autonomous Mode
            MESSAGE = "auto"
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
        # Motor voltage setting
        elif (event.type == KEYUP):
            if (event.key == K_0):
                MESSAGE = "0"
            elif (event.key == K_1):
                MESSAGE = "1"
            elif (event.key == K_2):
                MESSAGE = "2"
            elif (event.key == K_3):
                MESSAGE = "3"
            elif (event.key == K_4):
                MESSAGE = "4"
            elif (event.key == K_5):
                MESSAGE = "5"
            elif (event.key == K_6):
                MESSAGE = "6"
            elif (event.key == K_7):
                MESSAGE = "7"
            elif (event.key == K_8):
                MESSAGE = "8"
            elif (event.key == K_9):
                MESSAGE = "9"
        elif (event.type == pygame.QUIT):
            MESSAGE = "kill"
        else:
            MESSAGE = "w"
    
    if ((MESSAGE != "w") and (MESSAGE != "kill")):
        print MESSAGE
        s.send(MESSAGE)
    if (MESSAGE == "kill"):
        s.send("kill")
        pygame.quit()
        sys.exit()
        break

s.close()
