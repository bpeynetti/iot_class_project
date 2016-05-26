from __future__ import division
import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 15
ECHO = 21

file = open('log_data.csv','w')
file.write('Second,Avg_distance_per_sec,std_dev_per_second\n')


def get_measurements(data,second):

    this_second = [x for x in data if int(x[0]) == second]
    second_data = [x[1] for x in this_second]
    print "Second: ",second," Avg: ", (sum(second_data)/len(second_data))




measurements = []

start  = time.time()
prev_second = int(time.time())

print "distance measurement in progress"
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG,False)
print GPIO.input(ECHO)
time.sleep(2)
for i in range(1000):
    time.sleep(.1)
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

    measurements.append([time.time() - start, distance ])
    now = int(time.time())
    if (now > prev_second):
        get_measurements(measurements,now)
        prev_second = now 

    measurements = [x for x in measurements if x[0]>(now-60)]
    # print "Distance:",distance,"cm, time: ",pulse_dur
GPIO.cleanup()

