# -*- coding: utf-8 -*-
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

GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

file = open('log_data_change.csv','w')
file.write('Avg,Avg_diff,Std_dev,std_dev_20sec_avg,label\n')

file1 = open('unfiltered_data.csv','w')
file1.write('time,distance\n')

txt =''
txt_all = ''
def get_measurements(data,second):

    this_second = [x for x in data if x[0] > (second-5.0)]
    second_data = [x[1] for x in this_second]
    median_data = median(second_data)
    filtered_data = [x for x in second_data if abs(x-median_data)/median_data < 1]

    if (len(filtered_data)<2):
        print "no data"
        return
    return mean(filtered_data),standard_deviation(filtered_data)

import thread
def input_thread(L):
    raw_input()
    L.append(None)


events = ['chair_away','chair_close','occupied_away','occupied_close']
prev_avg = 0
std_dev_data = []
#for event in ['chair_away','chair_close','occupied_away','occupied_close']:
while 1:
    i = int(raw_input())
    while (i>=4):
        i = int(raw_input())
    if (i<0):
        break
    event = events[i]
    print "PLEASE PUT IN STATE:",event
    time.sleep(5)
    print 3 
    time.sleep(1)
    print 2 
    time.sleep(1)
    print 1 
    time.sleep(1)
    print "MEASURING"
    L = []
    thread.start_new_thread(input_thread,(L,))
    while not L:
        measurements = []
        GPIO.output(TRIG,False)
        time.sleep(1)
        start  = time.time()
        prev_second = int(time.time()-start)
        i=0
        while not L:
            i+=1
            time.sleep(.01)
            if (i%20==0):
                print i,'out of 1500 - TIME ELAPSED:',int(time.time()-start)
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
                avg,std_dev = get_measurements(measurements,time.time()-start)
                prev_second = now 
                if len(std_dev_data)==4:
                    # add to back of the list
                    std_dev_data = std_dev_data[1:]
                std_dev_data.append(std_dev)
                avg_diff = avg - prev_avg 
                prev_avg = avg
                print str(avg)+','+str(avg_diff)+','+str(std_dev)+','+str(mean(std_dev_data))+','+event
                txt += str(avg)+','+str(avg_diff)+','+str(std_dev)+','+str(mean(std_dev_data))+','+event+'\n'

            measurements = [x for x in measurements if x[0]>((time.time()-start)-10)]
            #print "Distance:",distance,"cm, time: ",pulse_dur
            txt_all += str(time.time())+','+str(distance)+'\n'

file.write(txt)
file1.write(txt_all)
GPIO.cleanup()

