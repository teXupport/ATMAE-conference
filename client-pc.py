import pygame, sys, math, random, time, socket, serial
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((800,400))
TCP_IP = '192.168.1.127'
TCP_PORT = 5022
BUFFER_SIZE = 256
MESSAGE = "w"
driveL = ""
driveR = ""
data = ""
##arduino = serial.Serial('/dev/ttyACM0', 115200, timeout = .1)  # Raspberry Pi
arduino = serial.Serial('COM4', 115200, timeout = .1)  # Windows computer

xBoxController = {}
pygame.joystick.init()                  # initializes the joysticks
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
for joy in joysticks:
  joy.init()

def JoystickAnalyizer(joystick):      #returns a dictionary for each player on the status of the controller
  joystickValues = {}
  axes = joystick.get_numaxes()
  buttons = joystick.get_numbuttons()
  hats = joystick.get_numhats()
  for i in range( axes ):
    axis = joystick.get_axis( i )
    axis = axis * 10.0
    math.floor(axis)
    if (axis < 0):
        axis = 0
    joystickValues["Axis{}".format(i)] = axis
  for i in range( buttons ):
    button = joystick.get_button( i )
    joystickValues["Button{}".format(i)] = button
  for i in range( hats ):
    hat = joystick.get_hat(i)
    joystickValues["Hat{}".format(i)] = hat
  
  return joystickValues


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

while 1:
    MESSAGE = "w"
    ## Xbox Controller
    xBoxController = JoystickAnalyizer(joysticks[0])
    if ((driveL != "B") and (xBoxController["Axis0"] > 0)):
        driveL == "F"
        MESSAGE = "L" + str(xBoxController["Axis0"])
        s.send(MESSAGE.encode())
    if ((driveR != "B") and (xBoxController["Axis1"] > 0)):
        driveR == "F"
        MESSAGE = "R" + str(xBoxController["Axis1"])
        s.send(MESSAGE.encode())
    if ((xBoxController["Axis0"] == 0) and (xBoxController["Button0"] == 0)):
        driveL = ""
        MESSAGE = "L0"
        s.send(MESSAGE.encode())
    if ((xBoxController["Axis1"] == 0) and (xBoxController["Button1"] == 0)):
        driveR = ""
        MESSAGE = "R0"
        s.send(MESSAGE.encode())
    if ((driveL != "F") and (xBoxController["Button0"] == 1)):
        driveL == "B"
        MESSAGE = "l"
        s.send(MESSAGE.encode())
    if ((driveR != "F") and (xBoxController["Button1"] == 1)):
        driveR == "B"
        MESSAGE = "r"
        s.send(MESSAGE.encode())
    
    for event in pygame.event.get():
        if (event.type == JOYBUTTONUP and (xBoxController["Button0"] == 1)):   ## Autonomous Mode
            MESSAGE = "t"
        elif (event.type == JOYBUTTONUP and (xBoxController["Button1"] == 1)):  ## Conveyor
            MESSAGE = "c"
        elif (event.type == JOYBUTTONUP and (xBoxController["Button2"] == 1)):    ## Brush
            MESSAGE = "b"
        elif (event.type == JOYBUTTONUP and (xBoxController["Button3"] == 1)):   ## Swing Arm
            MESSAGE = "y"
        elif (event.type == JOYBUTTONUP and (xBoxController["Button4"] == 1)):  ## PickUp Dustpan
            MESSAGE = "h"
        elif (event.type == JOYBUTTONUP and (xBoxController["Button5"] == 1)):    ## Dump and Reset Dustpan
            MESSAGE = "n"
        elif (event.type == JOYBUTTONUP and (xBoxController["Button6"] == 1)):    ## Arm Control
            flag = True
            MESSAGE = "u"
            s.send(MESSAGE.encode())
            while flag:
                    for event in pygame.event.get():
                            if (event.type == JOYBUTTONUP and (xBoxController["Button6"] == 1)):
                                    flag = False
                                    MESSAGE = "u"
                                    s.send(MESSAGE.encode())

                    if flag:
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
'''    ## KeyBoard
    for event in pygame.event.get():     
        if (((event.type == KEYDOWN) or event.type == KEYUP) and event.key == K_w):        ## Forward
            if (drive == ""):
                    drive = "w"
                    MESSAGE = "LR"
            elif (drive == "w"):
                    drive = ""
                    MESSAGE = "LR"
        elif (((event.type == KEYDOWN) or event.type == KEYUP) and event.key == K_s):   ## Back
            if (drive == ""):
                    drive = "s"
                    MESSAGE = "lr"
            elif (drive == "s"):
                    drive = ""
                    MESSAGE = "lr"
        elif (((event.type == KEYDOWN) or event.type == KEYUP) and event.key == K_a):    ## Left
            if (drive == ""):
                    drive = "a"
                    MESSAGE = "lR"
            elif (drive == "a"):
                    drive = ""
                    MESSAGE = "lR"
        elif (((event.type == KEYDOWN) or event.type == KEYUP) and event.key == K_d):   ## Right
            if (drive == ""):
                    drive = "d"
                    MESSAGE = "Lr"
            elif (drive == "d"):
                    drive = ""
                    MESSAGE = "Lr"
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
        elif (event.type == KEYUP and event.key == K_u):    ## Arm Control
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
'''
    if ((MESSAGE != "w") and (MESSAGE != "k")):
        print(MESSAGE)
        s.send(MESSAGE.encode())
    if (MESSAGE == "k"):
        s.send(MESSAGE.encode())
        pygame.quit()
        break
s.close()
sys.exit()
