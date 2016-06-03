# -*- coding: utf-8 -*-
from __future__ import division
import RPi.GPIO as GPIO
import time
import numpy
import random
import math
import thread
from useful_fn import *
GPIO.setmode(GPIO.BCM)

states = ['chair_away','chair_close','occupied_away','occupied_close']
TRIG = 15
ECHO = 21
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
file = open('log_data_change.csv','w')
file.write('time,prev_state,avg_diff, std_diff, new_state\n')

file1 = open('unfiltered_data.csv','w')
file1.write('time,distance\n')

txt =''
txt_all = ''

percentage_outliers = 5 # as a percentage 
sleep_time = 1 
time_interval = 5 
prev_second = int(time.time())
now = int(time.time())
start_time = int(time.time())
prev_state = states[0]

def input_thread(L):
    raw_input()
    L.append(None)

def get_data(time_interval, percentage_outliers):
    """ Samples the sensor for time_interval amount of seconds and then returns information"""
    GPIO.output(TRIG,False)
    start = int(time.time())
    now = int(start)
    measurements = []
    while (now - start < time_interval):
        now = int(time.time())
        time.sleep(.01)
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
            continue
        start_listen_1 = time.time()
        while GPIO.input(ECHO) == 1:
            pulse_end = time.time()
            if (pulse_end - start_listen_1)>0.01:
                flag = True
                break
        if flag==True:
            continue

        pulse_dur = pulse_end - pulse_start
        distance = pulse_dur * 17150
        if (distance>200):
            continue
        measurements.append([time.time() - start, distance ])

    # get avg, std deviation for the data (measurement array )
    data = [x[1] for x in measurements]
    # filter out top and bottom percent of outliers 
    bottom_outliers = [x for x in data if x<quantile(data,percentage_outliers/100)]
    top_outliers = [x for x in data if x>=quantile(data,(1-percentage_outliers/100))]
    outliers = bottom_outliers + top_outliers
    filtered_data = [x for x in data if x not in outliers]

    if (len(filtered_data)<2):
        print "no data"
        return

    return mean(filtered_data),standard_deviation(filtered_data)

prev_avg = 0
prev_std_dev = 0
while 1:
    print "Input new state that you will go to: "
    i = int(raw_input())
    while (i>=4):
        i = int(raw_input())
    if (i<0):
        break
    new_state = states[i]
    print "WAIT FOR START, THEN MOVE TO STATE:",new_state
    print 5 
    time.sleep(1)
    print 4
    time.sleep(1)
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
        now = int(time.time())
        avg,std_dev = get_data(time_interval,percentage_outliers)
        avg_diff = avg - prev_avg 
        std_diff = std_dev - prev_std_dev
        prev_avg = avg 
        prev_std_dev = std_dev 
        # record 
        txt = str(now-start_time)+','+prev_state+','+str(avg_diff)+','+str(std_diff)+','+new_state+'\n'
        prev_state = new_state 
        print txt," - CURR AVG: ",avg 
        file.write(txt)
        time.sleep(sleep_time)

GPIO.cleanup()

