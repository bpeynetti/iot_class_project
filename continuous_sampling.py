# -*- coding: utf-8 -*-
from __future__ import division
import RPi.GPIO as GPIO
import time
import numpy
import random
import math
import thread
from useful_fn import *
from classifier import *
GPIO.setmode(GPIO.BCM)
from firebase1 import Firebase
from myfirebase import * 

f = FirebaseClass()

print "Set file number"
num = int(raw_input())

states = ['chair_away','chair_close','occupied_away','occupied_close']
TRIG = 15
ECHO = 21
TRIG2 = 18
ECHO2 = 20
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(TRIG2, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
GPIO.setup(ECHO2, GPIO.IN)
file = open('data/log_data_change'+str(num)+'.csv','w')
file.write('time,prev_state,avg_diff,std_dev,std_diff, new_state\n')

file1 = open('unfiltered_data.csv','w')
file1.write('time,distance\n')

txt =''
txt_all = ''

percentage_outliers = 10 # as a percentage 
sleep_time = 1 
time_interval = 5
prev_second = int(time.time())
now = int(time.time())
start_time = int(time.time())
prev_state = states[0]

def send_data(allStates):
    """ thread that continuously polls and sends data whenenver the time is right """


    send_interval = 15
    # send the first element 
    f.add_state(0,True)
    f.add_state(0,False) 
    last_stable = 0 

    start_sending = time.time()
    last_time_sent = start_sending

    print "STARTING COMMM THREAD"
    while not L:
        if len(allStates)<1:
            continue
        if allStates[-1]!=last_stable:
            # print "STATE CHANGED: ",allStates[-1]
            if (allStates[-1]==allStates[-2]):
                print "NEW STATE STABLE, SENDING TRANSITION READING"
                last_stable = allStates[-1]
                f.add_state(last_stable,False)

        now = time.time()
        if (now - last_time_sent > send_interval):
            print "SENDING INTERVAL READING"
            f.add_state(last_stable,True)
	    last_time_sent = now




def input_thread(L):
    raw_input()
    L.append(None)

def get_data(time_interval, percentage_outliers):
    """ Samples the sensor for time_interval amount of seconds and then returns information"""
    GPIO.output(TRIG,False)
    GPIO.output(TRIG2,False)
    start = int(time.time())
    now = int(start)
    measurements = []
    measurements2 = []
    while (now - start < time_interval):
        #print now-start
        now = int(time.time())
        time.sleep(.01)

        # GET DISTANCE 
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
        #print (pulse_end-pulse_start)*17150

        # GET HEIGHT
        time.sleep(0.01)
        GPIO.output(TRIG2,True)
        time.sleep(0.00001)
        GPIO.output(TRIG2,False)
        start_listen_2 = time.time()
        flag = False
        while GPIO.input(ECHO2) == 0:
            pulse_start2 = time.time()
            if (pulse_start2 - start_listen_2)>.01:
                flag = True
                break
        if (flag==True):
            #print 'break1!'
            continue
        start_listen_3 = time.time()
        while GPIO.input(ECHO2) == 1:
            pulse_end2 = time.time()
            if (pulse_end2 - start_listen_3)>0.01:
                flag = True
                break
        if flag==True:
            #print 'breaking!'
            continue
        #print (pulse_end2-pulse_start2)*17150
            

        pulse_dur = pulse_end - pulse_start
        pulse_dur2 = pulse_end2 - pulse_start2 
        distance = pulse_dur * 17150
        distance2 = pulse_dur2 * 17150
        #print "Distance:",distance," - height: ",distance2
        if (distance>200):
            continue
        measurements.append([time.time() - start, distance ])
        measurements2.append([time.time() - start, distance2])

    # FOR DISTANCE 

    # get avg, std deviation for the data (measurement array )
    data = [x[1] for x in measurements]
    # filter out top and bottom percent of outliers 
    if standard_deviation(data)>.05:
        bottom_outliers = [x for x in data if x<quantile(data,percentage_outliers/100)]
        top_outliers = [x for x in data if x>=quantile(data,(1-percentage_outliers/100))]
        outliers = bottom_outliers + top_outliers
        filtered_data = [x for x in data if x not in outliers]
    else:
        filtered_data = data 
    

    # FOR HEIGHT 
    data2 = [x[1] for x in measurements2]
    if standard_deviation(data2)>.05:
        # filter out top and bottom percent of outliers 
        bottom_outliers2 = [x for x in data2 if x<quantile(data2,percentage_outliers/100)]
        top_outliers2 = [x for x in data2 if x>=quantile(data2,(1-percentage_outliers/100))]
        outliers2 = bottom_outliers2 + top_outliers2
        filtered_data2 = [x for x in data2 if x not in outliers2]
    else:
        filtered_data2 = data2

    if (len(filtered_data)<2) or len(filtered_data2)<2:
        print "no data"
        return mean(data),0,mean(data2),0


    return mean(filtered_data),standard_deviation(filtered_data),mean(filtered_data2),standard_deviation(filtered_data2)

prev_avg = 0
prev_avgH = 0 
prev_std_dev = 0
prev_std_devH = 0
avg_diff = 0 
avg_diffH = 0 
std_diff = 0 
std_diffH = 0 
allStates = []
allStates.append(0)
stable = 0
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
    thread.start_new_thread(send_data,(allStates,))
    while not L:
        now = int(time.time())
        avg,std_dev, avgH, std_devH = get_data(time_interval,percentage_outliers)
        # DISTANCE 
        avg_diff = avg - prev_avg 
        std_diff = std_dev - prev_std_dev
        prev_avg = avg 
        prev_std_dev = std_dev 
        # HEIGHT 
        avg_diffH = avgH - prev_avgH
        std_diffH = std_devH - prev_std_devH 
        prev_avgH = avgH 
        prev_std_devH = std_devH 

        predicted_state = get_new_state(states.index(prev_state), avg_diff, avgH, std_dev)
        allStates.append(predicted_state)
        if (len(allStates)>100):
            allStates = allStates[-100:]
        # f.add_state(states[predicted_state])
        # record 
        #this is the old version of the printing text
        #txt = str(now-start_time)+','+prev_state+','+str(avg_diff)+','+str(std_dev)+','+str(std_diff)+','+str(avgH)+','+str(avg_diffH)+','+str(std_devH)+','+str(std_diffH)+','+new_state+'\n'
        txt = str(now-start_time) + ',' + prev_state + ',' + str(states.index(prev_state)) + ',' + new_state + ',' + str(states.index(new_state)) + ',' + str(avg_diff) + ',' + str(avgH) +','+str(std_dev)+',' + str(predicted_state)
        print txt.strip()
        prev_state = states[predicted_state]
        file.write(txt)
        time.sleep(sleep_time)

GPIO.cleanup()

