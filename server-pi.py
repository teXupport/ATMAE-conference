#!/usr/bin/python

import socket, string, time, signal, sys
from Adafruit_PWM_Servo_Driver import PWM
from Adafruit_ADS1x15 import ADS1x15
##import RPi.GPIO as GPIO

##GPIO.setmode(GPIO.BCM)

##led = 4

chanBrush = 4
chanConveyor = 5
chanLeftMotor = 0
chanRightMotor = 1
chanSwingArm = 2
chanDustPan = 3

chanArmBase = 6
chanArmShoulder = 7
chanArmElbow = 8
chanArmClaw = 9

lm = 0
rm = 0
br = 0
cv = 0

TCP_IP = ''  # this is the server, so localhost
TCP_PORT = 5016  # port is the same on server and client
BUFFER_SIZE = 1024  # Normally 1024
   
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
auto = False  # initialize auto to False, meaning robot is not in autonomous mode
armModeb = False    # initialize armMode to False, meaning robot is not in arm mode

def signal_handler(signal, frame):
        print 'You pressed Ctrl+C!'
        
        # STOP all motors/servos
        pwm.setPWM(chanBrush, 0, 0)
        pwm.setPWM(chanConveyor, 0, 0)
        pwm.setPWM(chanLeftMotor, 0, 0)
        pwm.setPWM(chanRightMotor, 0, 0)
        pwm.setPWM(chanSwingArm, 0, 0)
        pwm.setPWM(chanDustPan, 0, 0)
        
        conn.close()  # close the connection
        sys.exit(0)  # exit gracefully
signal.signal(signal.SIGINT, signal_handler)
print 'Server(server.py) started'
print 'Press Ctrl+C to exit'

ADS1115 = 0x01  # 16-bit ADC

# Select the gain
gain = 6144  # +/- 6.144V
# gain = 5120  # +/- 5.120V
# gain = 4096  # +/- 4.096V
# gain = 2048  # +/- 2.048V
# gain = 1024  # +/- 1.024V
# gain = 512   # +/- 0.512V
# gain = 256   # +/- 0.256V

# Select the sample rate
# sps = 8    # 8 samples per second
# sps = 16   # 16 samples per second
# sps = 32   # 32 samples per second
# sps = 64   # 64 samples per second
# sps = 128  # 128 samples per second
sps = 250  # 250 samples per second
# sps = 475  # 475 samples per second
# sps = 860  # 860 samples per second

# Initialize the ADC using the default mode for ADS1115 (use default I2C address)
adc = ADS1x15(ic=ADS1115)

pwm = PWM(0x40)  # PWM controller is at I2C address 0x40
pwm.setPWMFreq(60)  # Set frequency to 60 Hz

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000  # 1,000,000 us per second
  pulseLength /= 60  # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096  # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

def armMode():
    global armModeb
    s.setblocking(0)  # prevent s.recv from blocking the code
    while armModeb:
        data = conn.recv(BUFFER_SIZE)
        if (string.find(data, "u") != -1):
                armModeb = False
                s.setblocking(1)  # allow s.recv to block again
                break
        elif (len(data) == 13):
                print data
                servo1 = int(float(data[0:3]))
                servo2 = int(float(data[3:6]))
                servo3 = int(float(data[6:9]))
                servo4 = int(float(data[9:12]))
                #print('%f, %f, %f, %f' % (servo1, servo2, servo3, servo4))
                        
                pwm.setPWM(chanArmBase, 0, (servo1*450/255+150))
                pwm.setPWM(chanArmShoulder, 0, (servo2*450/255+150))
                pwm.setPWM(chanArmElbow, 0, (servo3*450/255+150))
                pwm.setPWM(chanArmClaw, 0, (servo4*450/255+150))
                
def autonomousMode():
    global auto          # needed to globally change the value of auto
    s.setblocking(0)  # prevent s.recv from blocking the code
    pwm.setPWM(chanBrush, 0, servoMax)  # turn on brush
    while auto:
        data = conn.recv(BUFFER_SIZE)
        if (string.find(data, "auto") != -1):
                ##GPIO.output(led, 0)  # turn off autonomous mode indicator LED
                auto = False  # set auto to False, no longer autonomous
                pwm.setPWM(chanLeftMotor, 0, 0)  #STOP left motor
                pwm.setPWM(chanRightMotor, 0, 0)  #STOP right motor
                s.setblocking(1)  # allow s.recv to block again
                pwm.setPWM(chanBrush, 0, 0)  # turn off brush
                break
        else:
 # Do line following code <<---  Final Place for code!!!!!!!!!!!!!!!!!!
                voltsFL = adc.readADCSingleEnded(0, gain, sps) / 1000  # far left sensor
                voltsNL = adc.readADCSingleEnded(1, gain, sps) / 1000  # near left sensor
                voltsLM = adc.readADCSingleEnded(4, gain, sps) / 1000  # left middle sensor
                voltsRM = adc.readADCSingleEnded(5, gain, sps) / 1000  # right middle sensor
                voltsNR = adc.readADCSingleEnded(2, gain, sps) / 1000  # near right sensor
                voltsFR = adc.readADCSingleEnded(3, gain, sps) / 1000  # far right sensor

                if (((voltsFL/(gain/1000)) < .5) and ((voltsNL/(gain/1000)) < .5)):
                        pwm.setPWM(chanLeftMotor, 0, (servoMax-100))
                else:
                        pwm.setPWM(chanLeftMotor, 0, 0)
                                        
                if (((voltsLM/(gain/1000)) > .5) and ((voltsRM/(gain/1000)) > .5)):
                    pwm.setPWM(chanRightMotor, 0, (servoMax-100))
                    pwm.setPWM(chanLeftMotor, 0, (servoMax-100))
                else:
                    pwm.setPWM(chanRightMotor, 0, 0)
                    pwm.setPWM(chanLeftMotor, 0, 0)
                                        
                if (((voltsNR/(gain/1000)) < .5) and ((voltsFR/(gain/1000)) < .5)):
                        pwm.setPWM(chanRightMotor, 0, (servoMax-100))
                else:
                        pwm.setPWM(chanRightMotor, 0, 0)
    

while 1:
    s.listen(1)
        
    conn, addr = s.accept()
    print 'Connection address:', addr
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if (string.find(data, "t") != -1):
            # toggle autonomous
            if not auto:
                GPIO.output(led, 1)
                auto = True
                autonmousMode()
            else:
                pass
        if (string.find(data, "L") != -1):
            # left motor forward
            if(lm == 1):
                pwm.setPWM(chanLeftMotor, 0, 0)
                lm = 0
            else:
                pwm.setPWM(chanLeftMotor, 0, servoMax)
                lm = 1
        if (string.find(data, "R") != -1):
            # right motor forward
            if(rm == 1):
                pwm.setPWM(chanRightMotor, 0, 0)
                rm = 0
            else:
                pwm.setPWM(chanRightMotor, 0, servoMax)
                rm = 1
        if (string.find(data, "l") != -1):
            # left motor backward
            if(lm == -1):
                pwm.setPWM(chanLeftMotor, 0, 0)
                lm = 0
            else:
                pwm.setPWM(chanLeftMotor, 0, servoMin)
                lm = -1
        if (string.find(data, "r") != -1):
            # right motor backward
            if(rm == -1):
                pwm.setPWM(chanRightMotor, 0, 0)
                rm = 0
            else:
                pwm.setPWM(chanRightMotor, 0, servoMin)
                rm = -1
        if (string.find(data, "c") != -1):
            # toggle conveyor
            if(cv == 1):
                pwm.setPWM(chanConveyor, 0, 0)
                cv = 0
            else:
                pwm.setPWM(chanConveyor, 0, servoMax)
                cv = 1
        if (string.find(data, "b") != -1):
            # toggle brush
            if(br == 1):
                pwm.setPWM(chanBrush, 0, 0)
                br = 0
            else:
                pwm.setPWM(chanBrush, 0, servoMax)
                br = 1
        if (string.find(data, "y") != -1):
            # swing arm
            pwm.setPWM(chanSwingArm, 0, 2500)
            time.sleep(1)
            pwm.setPWM(chanSwingArm, 0, 500)
        if (string.find(data, "h") != -1):
            # pick up dustpan
            pwm.setPWM(chanDustPan, 0, 1200)
        if (string.find(data, "n") != -1):
            # dump and reset dustpan
            pwm.setPWM(pinDustPan, 0, 500)
            time.sleep(2)
            pwm.setPWM(pinDustPan, 0, 2500)
        if (string.find(data, "u") != -1):
                armModeb = True
                armMode()
        if (data == "k"):
            break
        print "received data:", data
        conn.send(data)  # echo
    print "Client disconnected"
    conn.close()
    if (data == "k"):
        break

#  STOP all motors/servos
pwm.setPWM(chanBrush, 0, 0)
pwm.setPWM(chanConveyor, 0, 0)
pwm.setPWM(chanLeftMotor, 0, 0)
pwm.setPWM(chanRightMotor, 0, 0)
pwm.setPWM(chanSwingArm, 0, 0)
pwm.setPWM(chanDustPan, 0, 0)
        
print "kill command received. Goodbye."
