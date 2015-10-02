import socket, string
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

led = 4

GPIO.setup(led, GPIO.OUT)

TCP_IP = '127.0.0.1'
TCP_PORT = 5012
BUFFER_SIZE = 1024  # Normally 1024
   
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
auto = False

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
            else:
                GPIO.output(led, 0)
                auto = False
##        elif (string.find(data, "L") != -1):
##            # left motor forward
##        elif (string.find(data, "R") != -1):
##            # right motor forward
##        elif (string.find(data, "l") != -1):
##            # left motor backward
##        elif (string.find(data, "r") != -1):
##            # right motor backward
##        elif (string.find(data, "c") != -1):
##            # toggle conveyor
##        elif (string.find(data, "b") != -1):
##            # toggle brush
##        elif (string.find(data, "y") != -1):
##            # swing arm
##        elif (string.find(data, "h") != -1):
##            # pick up dustpan
##        elif (string.find(data, "n") != -1):
            # dump and reset dustpan
        elif (data == "exit"):
            break
        elif (data == "kill"):
            break
        print "received data:", data
        conn.send(data)  # echo
    print "Client disconnected"
    conn.close()
    if (data == "kill"):
        break

print "kill command received. Goodbye."
