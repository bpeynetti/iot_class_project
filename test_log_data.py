from __future__ import division
import RPi.GPIO as GPIO
import time
import numpy
import random
import math
from useful_fn import *
GPIO.setmode(GPIO.BCM)

TRIG = 15
ECHO = 21

file = open('log_data.csv','w')
file.write('Second,Avg_distance_per_sec,std_dev_per_second\n')

file1 = open('unfiltered_data.csv','w')
file1.write('time,distance\n')

txt =''
txt_all = ''
def get_measurements(data,second):

    # print (second-1)

    this_second = [x for x in data if x[0] > (second-2.0)]
    # print this_second

    second_data = [x[1] for x in this_second]
    median_data = median(second_data)
    filtered_data = [x for x in second_data if abs(x-median_data)/median_data < 1]
    #for i in this_second:
    #    print i
    if (len(filtered_data)<2):
        print "no data"
        return
    #print len(filtered_data)
    #print len(second_data)-len(filtered_data)
    #print "Second: ",second," Avg: ", mean(filtered_data), " STD_DEV: ",standard_deviation(filtered_data)
    global txt
    txt += str(int(second))+','+str(mean(filtered_data))+','+str(standard_deviation(filtered_data))+'\n'

    # return mean(filtered_data)

measurements = []



print "distance measurement in progress"
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.output(TRIG,False)
print GPIO.input(ECHO)
time.sleep(3)
start  = time.time()
prev_second = int(time.time()-start)
for i in range(3000):
    time.sleep(.01)
    if (i%20==0):
        print i,'out of 3000 - TIME ELAPSED:',int(time.time()-start)
    GPIO.output(TRIG,True)
    time.sleep(0.00001)
    GPIO.output(TRIG,False)
    start_listen_0 = time.time()
    flag = False
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
        if (pulse_start - start_listen_0)>.01:
            flag = True
            break
    if (flag==True):
        #print "FAILED READING"
        continue
    start_listen_1 = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
        if (pulse_end - start_listen_1)>0.01:
            flag = True
            break
    if flag==True:
        #print "FAILED READING"
        continue
    # pulse_end = random.random()
    # pulse_start = random.random()
    pulse_dur = pulse_end - pulse_start
    distance = pulse_dur * 17150
    distance = round(distance, 3)
    if (distance>200):
        continue
    measurements.append([time.time() - start, distance ])
    now = int(time.time()-start)
    # print now,prev_second,len(measurements),measurements
    if (now > prev_second) and len(measurements)>5:
        get_measurements(measurements,time.time()-start)
        prev_second = now 

    measurements = [x for x in measurements if x[0]>((time.time()-start)-5)]
    #print "Distance:",distance,"cm, time: ",pulse_dur
    txt_all += str(time.time())+','+str(distance)+'\n'

file.write(txt)
file1.write(txt_all)
GPIO.cleanup()

