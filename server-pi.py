import socket, string, time, pigpio

led = 4
pi = pigpio.pi()
pinSwingArm = 16
pinDustPan = 19
pinBrush = 17
pinConveyor = 18
pinLeftMotor = 13
pinRightMotor = 6

pi.set_mode(pinSwingArm, pigpio.OUTPUT)
pi.set_mode(pinDustPan, pigpio.OUTPUT)
pi.set_mode(pinBrush, pigpio.OUTPUT)
pi.set_mode(pinConveyor, pigpio.OUTPUT)
pi.set_mode(pinLeftMotor, pigpio.OUTPUT)
pi.set_mode(pinRightMotor, pigpio.OUTPUT)

pi.set_PWM_dutycycle(pinLeftMotor, 127)
pi.set_PWM_dutycycle(pinRightMotor, 127)
pi.set_PWM_dutycycle(pinConveyor, 127)
pi.set_PWM_dutycycle(pinBrush, 127)

TCP_IP = '127.0.0.1'
TCP_PORT = 5010
BUFFER_SIZE = 1024  # Normally 1024
   
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
auto = False

def autonomousMode():
   global auto          # needed to globally change the value of Auto
   while auto:
	   data = conn.recv(BUFFER_SIZE)
      if (string.find(data, "auto") != -1):
         GPIO.output(led, 0)
         auto = False
         break
      else:
         # Do line following code <<---  Final Place for code!!!!!!!!!!!!!!!!!!
         pass
	
    

while 1:
    s.listen(1)
        
    conn, addr = s.accept()
    print 'Connection address:', addr
    while 1:
        data = conn.recv(BUFFER_SIZE)
        if (string.find(data, "auto") != -1):
            # toggle autonomous
            if not auto:
                GPIO.output(led, 1)
                auto = True
                autonmousMode()
            else:
                pass
        if (string.find(data, "L") != -1):
            # left motor forward
            if (pi.get_PWM_dutycycle(pinLeftMotor) != 127):
                pi.set_PWM_dutycycle(pinLeftMotor, 127)
            else:
                pi.set_PWM_dutycycle(pinLeftMotor, 255)
        if (string.find(data, "R") != -1):
            # right motor forward
            if (pi.get_PWM_dutycycle(pinRightMotor) != 127):
                pi.set_PWM_dutycycle(pinRightMotor, 127)
            else:
                pi.set_PWM_dutycycle(pinRightMotor, 255)
        if (string.find(data, "l") != -1):
            # left motor backward
            if (pi.get_PWM_dutycycle(pinLeftMotor) != 127):
                pi.set_PWM_dutycycle(pinLeftMotor, 127)
            else:
                pi.set_PWM_dutycycle(pinLeftMotor, 0)
        if (string.find(data, "r") != -1):
            # right motor backward
            if (pi.get_PWM_dutycycle(pinRightMotor) != 127):
                pi.set_PWM_dutycycle(pinRightMotor, 127)
            else:
                pi.set_PWM_dutycycle(pinRightMotor, 0)
        if (string.find(data, "c") != -1):
            # toggle conveyor
            if (pi.get_PWM_dutycycle(pinConveyor) != 127):
                pi.set_PWM_dutycycle(pinConveyor, 127)
            else:
                pi.set_PWM_dutycycle(pinConveyor, 255)
        if (string.find(data, "b") != -1):
            # toggle brush
            if (pi.get_PWM_dutycycle(pinBrush) != 127):
                pi.set_PWM_dutycycle(pinBrush, 127)
            else:
                pi.set_PWM_dutycycle(pinBrush, 255)
        if (string.find(data, "y") != -1):
            # swing arm
            pi.set_servo_pulsewidth(pinSwingArm, 2500)
            time.sleep(1)
            pi.set_servo_pulsewidth(pinSwingArm, 500)
        if (string.find(data, "h") != -1):
            # pick up dustpan
            pi.set_servo_pulsewidth(pinDustPan, 1200)
        if (string.find(data, "n") != -1):
            # dump and reset dustpan
            pi.set_servo_pulsewidth(pinDustPan, 500)
            time.sleep(2)
            pi.set_servo_pulsewidth(pinDustPan, 2500)
        if (data == "exit"):
            break
        if (data == "kill"):
            break
        print "received data:", data
        conn.send(data)  # echo
    print "Client disconnected"
    conn.close()
    if (data == "kill"):
        break

print "kill command received. Goodbye."
