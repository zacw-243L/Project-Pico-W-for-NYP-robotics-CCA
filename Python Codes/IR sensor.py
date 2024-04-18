from time import sleep
from machine import Pin
import random

Mot_A_Forward = Pin(18, Pin.OUT)
Mot_A_Back = Pin(19, Pin.OUT)
Mot_B_Forward = Pin(20, Pin.OUT)
Mot_B_Back = Pin(21, Pin.OUT)
sensor = Pin(3, Pin.IN)

def move_forward():
    Mot_A_Forward.value(1)
    Mot_B_Forward.value(1)
    Mot_A_Back.value(0)
    Mot_B_Back.value(0)
    
def move_backward():
    Mot_A_Forward.value(0)
    Mot_B_Forward.value(0)
    Mot_A_Back.value(1)
    Mot_B_Back.value(1)

def move_stop():
    Mot_A_Forward.value(0)
    Mot_B_Forward.value(0)
    Mot_A_Back.value(0)
    Mot_B_Back.value(0)

def move_left():
    Mot_A_Forward.value(1)
    Mot_B_Forward.value(0)
    Mot_A_Back.value(0)
    Mot_B_Back.value(1)

def move_right():
    Mot_A_Forward.value(0)
    Mot_B_Forward.value(1)
    Mot_A_Back.value(1)
    Mot_B_Back.value(0)

movement_functions = [move_backward, move_left, move_right]
movement_function = [move_forward, move_left, move_right]
x = random.choice(movement_functions)
y = random.choice(movement_function)

while True:
    if sensor.value() == 1:
        print("1")
        y = random.choice(movement_function)
        y()
        sleep(1)
        move_stop()
    if sensor.value() == 0:
        print("0")
        x = random.choice(movement_functions)
        x()
        sleep(1)
        move_stop()
