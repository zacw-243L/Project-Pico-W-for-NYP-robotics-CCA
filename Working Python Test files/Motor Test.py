from time import sleep
from machine import PWM, Pin

Mot_A_Forward = Pin(18, Pin.OUT)
Mot_A_Back = Pin(19, Pin.OUT)
Mot_B_Forward = Pin(20, Pin.OUT)
Mot_B_Back = Pin(21, Pin.OUT)

# Set PWM
EN_A = PWM(Pin(8))
EN_B = PWM(Pin(2))
# Defining frequency for enable pins
EN_A.freq(1500)
EN_B.freq(1500)
# Setting maximum duty cycle for maximum speed (0 to 65025)
EN_A.duty_u16(65025)
EN_B.duty_u16(65025)

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

move_stop()
sleep(2)

print ("Forward test")

move_forward()
sleep(2)

print ("Backward test")

move_backward()
sleep(2)

print ("Spin left test")

move_left()
sleep(2)

print ("Spin right test")

move_right()
sleep(2)

print ("'Time for bed' said Zeberdee.")

move_stop()