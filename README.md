# Roboto Project for NYP robotics CCA
<br>
Repository for all things needed for the robot to work
<br>

## Below are the steps taken to make the robot

<br>

 1. [link to tutorial](https://www.explainingcomputers.com/pi_pico_w_robot.html "explainingcomputer's Pi Pico W WiFi Controlled Robot") this is where to get the base code for the bot

 2. [video showing how to build the bot](https://youtu.be/iTo4Qh2R6m4) <br> Requires: Flathead Screwdriver, Wire Cutters, 3D Printers, Allen Wrench, Solder, Soldering Iron, Female to Female jumper wires (short)<br>

### Youtube tutorial

[![Raspberry Pi Pico W: WiFi  Controlled Robot](https://i.ytimg.com/vi/iTo4Qh2R6m4/maxresdefault.jpg)](https://www.youtube.com/watch?v=iTo4Qh2R6m4 "Raspberry Pi Pico W: WiFi  Controlled Robot")   
 

 3. [link to thonny micropython IDE](https://thonny.org/)

 4. [link to micropython pico W](https://micropython.org/download/RPI_PICO_W/)

 5. [link to reset the pico w](https://github.com/dwelch67/raspberrypi-pico/blob/main/flash_nuke.uf2) hopefully optional

<br>

## IR sensor code

```
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
```
