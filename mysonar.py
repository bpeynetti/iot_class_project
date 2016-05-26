import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 15
ECHO = 21

print "distance measurement in progress"
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG,False)
print GPIO.input(ECHO)
time.sleep(2)
for i in range(300):
    time.sleep(.5)
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_dur = pulse_end - pulse_start
    distance = pulse_dur * 17150
    distance = round(distance, 3)
    print "Distance:",distance,"cm, time: ",pulse_dur
GPIO.cleanup()

