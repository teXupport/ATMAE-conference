#!/usr/bin/python

import socket, string, time, signal, sys
from Adafruit_PWM_Servo_Driver import PWM
from Adafruit_ADS1x15 import ADS1x15
##import RPi.GPIO as GPIO

##GPIO.setmode(GPIO.BCM)

##led = 4

chanLeftMotor = 0
chanRightMotor = 1
chanLeftDoor = 2
chanRightDoor = 3
chanLeftFlipper = 4
chanRightFlipper = 5

lm = 0
rm = 0
ld = 0
rd = 0

TCP_IP = ''  # this is the server, so localhost
TCP_PORT = 5026  # port is the same on server and client
BUFFER_SIZE = 32  # Normally 1024
   
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
auto = False  # initialize auto to False, meaning robot is not in autonomous mode

def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'

    # STOP all motors/servos
    pwm.setPWM(chanLeftDoor, 0, 0)
    pwm.setPWM(chanRightDoor, 0, 0)
    pwm.setPWM(chanLeftMotor, 0, 0)
    pwm.setPWM(chanRightMotor, 0, 0)
    pwm.setPWM(chanLeftFlipper, 0, 0)
    pwm.setPWM(chanRightFlipper, 0, 0)

    conn.close()  # close the connection
    sys.exit(0)  # exit gracefully

signal.signal(signal.SIGINT, signal_handler)
print 'Server(server.py) started'
print 'Press Ctrl+C to exit'

ADS1115 = 0x01  # 16-bit ADC

# Select the gain
# gain = 6144  # +/- 6.144V
# gain = 5120  # +/- 5.120V
gain = 4096  # +/- 4.096V
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
servoMax = 650  # Max pulse length out of 4096
motorMax = 650
motorMin = 150
reverseSpeed = 0.8 # between 0 and 1

def setServoPulse(channel, pulse):
    pulseLength = 1000000  # 1,000,000 us per second
    pulseLength /= 60  # 60 Hz
    print "%d us per period" % pulseLength
    pulseLength /= 4096  # 12 bits of resolution
    print "%d us per bit" % pulseLength
    pulse *= 1000
    pulse /= pulseLength
    pwm.setPWM(channel, 0, pulse)
                
def autonomousMode():
    global auto          # needed to globally change the value of auto
    global data, s, pwm, chanLeftMotor, chanRightMotor, conn
    auto = True
    data = ""
    print 'Autonomous mode entered.'
    motorMax = 650
    s.setblocking(0)  # prevent s.recv from blocking the code
    count = 0
    while auto:
        data = conn.recv(BUFFER_SIZE)
        if (string.find(data, "t") != -1):
            ##GPIO.output(led, 0)  # turn off autonomous mode indicator LED
            auto = False  # set auto to False, no longer autonomous
            pwm.setPWM(chanLeftMotor, 0, 0)  #STOP left motor
            pwm.setPWM(chanRightMotor, 0, 0)  #STOP right motor
            s.setblocking(1)  # allow s.recv to block again
            break
        else:
# Do line following code <<---  Final Place for code!!!!!!!!!!!!!!!!!!
            #voltsFL = adc.readADCSingleEnded(0, gain, sps) / 1000  # far left sensor
            voltsNL = adc.readADCSingleEnded(0, gain, sps) / 1000 # near left sensor
            #voltsLM = adc.readADCSingleEnded(4, gain, sps) / 1000  # left middle sensor
            #voltsRM = adc.readADCSingleEnded(5, gain, sps) / 1000  # right middle sensor
            #voltsNR = adc.readADCSingleEnded(2, gain, sps) / 1000  # near right sensor
            voltsFR = adc.readADCSingleEnded(2, gain, sps) / 1000 # far right sensor
            voltsRM = (voltsNL + voltsFR) / 2
            if (count >= 0):
                print voltsNL
                print voltsFR
                print voltsRM
                count = count + 1
            #if (((voltsFL/(gain/1000)) < .5) and ((voltsNL/(gain/1000)) < .5)):
            if (voltsNL < 3):
                pwm.setPWM(chanLeftMotor, 0, (motorMax-300))
            else:
                pwm.setPWM(chanLeftMotor, 0, 0)
                                    
            #if (((voltsLM/(gain/1000)) > .5) and ((voltsRM/(gain/1000)) > .5)):
            if (voltsRM < 3):
                pwm.setPWM(chanRightMotor, 0, (motorMax-300))
                pwm.setPWM(chanLeftMotor, 0, (motorMax-300))
            else:
                pwm.setPWM(chanRightMotor, 0, 0)
                pwm.setPWM(chanLeftMotor, 0, 0)
                                    
            #if (((voltsNR/(gain/1000)) < .5) and ((voltsFR/(gain/1000)) < .5)):
            if (voltsFR < 3):
                pwm.setPWM(chanRightMotor, 0, (motorMax-300))
            else:
                pwm.setPWM(chanRightMotor, 0, 0)
    
leftVal, rightVal = (0,0)
while 1:
    s.listen(1)
        
    conn, addr = s.accept()
    print 'Connection address:', addr
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if (string.find(data, "t") != -1):
            # toggle autonomous
            if not auto:
                #GPIO.output(led, 1)
                auto = True
                autonomousMode()
            else:
                pass
        if (string.rfind(data, "L") != -1):
            # left motor forward
              if(string.rfind(data, "L0") == -1):
                  leftVal = int(data[string.rfind(data, "L")+1:string.rfind(data, "L")+4])
              else:
                  leftVal = 0
        if (string.rfind(data, "R") != -1):
            # right motor forward
              if(string.rfind(data, "R0") == -1):
                  rightVal = int(data[string.rfind(data, "R")+1:string.rfind(data, "R")+4])
              else:
                  rightVal = 0
        if (string.find(data, "l") != -1):
            # left motor backward
            if(lm == -1):
                leftVal = 0
                lm = 0
            else:
                leftVal = int(round(((motorMax-motorMin) / 2 - reverseSpeed * (motorMax-motorMin) / 2), 0))
                lm = -1
        if (string.find(data, "r") != -1):
            # right motor backward
            if(rm == -1):
                rightVal = 0
                rm = 0
            else:
                rightVal = int(round(((motorMax-motorMin) / 2 - reverseSpeed * (motorMax-motorMin) / 2), 0))
                rm = -1
        if (string.find(data, "D") != -1):
            # toggle left door
            if(ld == 1):
                pwm.setPWM(chanLeftDoor, 0, servoMin)
                ld = 0
            else:
                pwm.setPWM(chanLeftDoor, 0, servoMax)
                ld = 1
        if (string.find(data, "d") != -1):
            # toggle right door
            if(rd == 1):
                pwm.setPWM(chanRightDoor, 0, servoMin)
                rd = 0
            else:
                pwm.setPWM(chanRightDoor, 0, servoMax)
                rd = 1
        if (string.find(data, "f") != -1):
            # engage flipper
            pwm.setPWM(chanLeftFlipper, 0, servoMax)
	    pwm.setPWM(chanRightFlipper, 0, servoMin)
            time.sleep(1)
            pwm.setPWM(chanLeftFlipper, 0, servoMin)
	    pwm.setPWM(chanRightFlipper, 0, servoMax)
        if (string.find(data, "m") != -1):
            pwm.setPWM(chanLeftFlipper, 0, (servoMin + servoMax)/2)
	    pwm.setPWM(chanRightFlipper, 0, (servoMin + servoMax)/2)
	if (string.find(data, "q") != -1):
	    for x in range(5):
	        pwm.setPWM(chanLeftFlipper, 0, servoMax)
	        pwm.setPWM(chanRightFlipper, 0, servoMax)
	        time.sleep(1)
	        pwm.setPWM(chanLeftFlipper, 0, servoMin)
	        pwm.setPWM(chanRightFlipper, 0, servoMin)
	        time.sleep(1)
        if (string.find(data, "k") != -1):
            break
        print "received data:", data
        conn.send(data)  # echo
        pwm.setPWM(chanLeftMotor, 0, leftVal)
        pwm.setPWM(chanRightMotor, 0, rightVal)
    print "Client disconnected"
    conn.close()
    if (string.find(data, "k") != -1):
        break

#  STOP all motors/servos
pwm.setPWM(chanLeftDoor, 0, 0)
pwm.setPWM(chanRightDoor, 0, 0)
pwm.setPWM(chanLeftMotor, 0, 0)
pwm.setPWM(chanRightMotor, 0, 0)
pwm.setPWM(chanLeftFlipper, 0, 0)
pwm.setPWM(chanRightFlipper, 0, 0)
        
print "kill command received. Goodbye."
