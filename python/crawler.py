# crawler.py
# ----------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice
# this code has been designed by a group of students in Tehran University, faculty of Mechanical engineering 
# you can contact us by email: ahmednabipour@ut.ac.ir or parham.kazemi@ut.ac.ir or mahdi.hallajian@ut.ac.ir


import numpy as np
import scipy.optimize as optimize
import time
import serial
import random
ser = serial.Serial()       
ser.baudrate = 9600
ser.port = 'COM14'              # find out that ardunio is connect to whcih one of the COMs (you can use arduino IDE)
ser.open()
while True:                     # make sure that arduino is ready for serial communication
    income = ser.readline()
    ser.flush() 
    serial_stat = income.decode('utf-8')
    if serial_stat == "ready\r\n" :
        break
state1_reward_dict = {}
state2_reward_dict = {}
trace_back_state = np.zeros((3,2))
trace_back_func = np.zeros((3,1))

def roll_forward_state(trace_back_state, a, b):
    k = 1
    for i in range(0,2):
        for j in range (0,2):
            trace_back_state[k+1][j] = trace_back_state[k][j]
        k = k - 1
    trace_back_state[0][0] = a
    trace_back_state[0][1] = b

def roll_forward_func(trace_back_func, reward):
    k = 1
    for i in range(0,2):
        trace_back_func[k+1][0] = trace_back_func[k][0]
        k = k - 1
    trace_back_func[0][0] = reward

def f(params):
    a, b = params 
    if a > 90 or b > 120:
        return (0)
    reward = arduino(a, b)
    print(trace_back_state)
    roll_forward_state(trace_back_state, a, b)
    roll_forward_func(trace_back_func, reward)
    return reward 

def greedy():           # this is the greedy function which tell the robot to do the best action which u know until now
    if iteration == 1:
        optimize.minimize(f, initial_guess,(),'Nelder-Mead',None,None,5)        # we have changed the simplex method constants as the following:
        print("first iteration has been finished")                              # rho = 1.2  chi = 2     psi = 0.5   sigma = 0.5     nonzdelt = 1    zdelt = 0.00025
    else:                                                                       # we have also changed some parts of the scipy nelder_mead library. The nones are those changed
        print("I am not in first iteration any more")                           # parts which are not needed. in this line 8 is the max_iteration and trace_back_state is the initial simplex
        optimize.minimize(f, initial_guess,(),'Nelder-Mead',None,None,8,trace_back_state)

def explore():          # makes the robot to explore so to make sure the robot has seen all the states
    while True:
        print("I am exploring")
        servo1_angle = random.SystemRandom().randint(0 , 90)
        servo2_angle = random.SystemRandom().randint(0 , 110)
        if servo1_angle not in state1_reward_dict.keys() and servo2_angle not in state2_reward_dict.keys():
            encoder_reward = arduino(servo1_angle, servo2_angle)
            print(encoder_reward)
            reward_max = min(state1_reward_dict.values())
            if encoder_reward <= reward_max :
                print("I found a better solution")
                initial_guess = [servo1_angle, servo2_angle]
                optimize.minimize(f, initial_guess,(),'Nelder-Mead',None,None,5)
            state1_reward_dict[servo1_angle] = encoder_reward
            state2_reward_dict[servo2_angle] = encoder_reward
            break                

def arduino(servo1, servo2):        #send the string which contains 2 numbers, the angle of Servo1 and 2
    servo1 = str(servo1)
    servo2 = str(servo2)
    out = servo1 + "&" + servo2
    out_byt = bytes(out, 'utf-8')
    ser.write(out_byt)
    inp = ser.readline()
    ser.flush() 
    str_inp = inp.decode('utf-8')
    reward = float(str_inp)
    return (reward)


while 1 :               # the infinit loop of learning :D
    servo1_angle = random.SystemRandom().randint(0 , 90)        #randomly tryes some angles inorder to find an angle which the robot moves forward
    servo2_angle = random.SystemRandom().randint(0 , 110)       #after that it tries to learn better solutins by using its experience and downhill simplex method
    if servo1_angle not in state1_reward_dict.keys() and servo2_angle not in state2_reward_dict.keys():                     
        encoder_reward = arduino(servo1_angle, servo2_angle) #  take reward from arduino
        initial_guess = [servo1_angle, servo2_angle]
        state1_reward_dict[servo1_angle] = encoder_reward
        state2_reward_dict[servo2_angle] = encoder_reward
    if encoder_reward != 0 :
        iteration = 0
        while 1:
            iteration = iteration + 1
            epsilon = 0.3
            p = np.random.uniform(0 , 1)
            if iteration > 1:
                if p >= epsilon :
                    greedy()
                else :
                    explore()
            else:
                greedy()
            print(iteration)

#[[80.91282574 82.2934859 ]
# [80.92403057 82.30225818]             best last number
# [80.92835398 82.30476674]]
#[[81.83376125 71.15413063]
# [82.63100859 69.3039418 ]
# [82.14011875 70.42505938]]