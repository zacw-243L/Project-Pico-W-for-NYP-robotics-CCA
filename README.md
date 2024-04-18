# Roboto Project for NYP robotics CCA
<br>
Repository for all things needed for the robot to work
<br>

## Below are the steps taken to make the robot

<br>

 1. [link to tutorial](https://www.explainingcomputers.com/pi_pico_w_robot.html "explainingcomputer's Pi Pico W WiFi Controlled Robot") this is where to get the base code for the bot

 2. [video showing how to build the bot](https://youtu.be/iTo4Qh2R6m4) <br> Requires: Flathead Screwdriver, Wire Cutters, 3D Printers, Allen Wrench, Solder, Soldering Iron, Female to Female jumper wires (short)<br>

### Youtube tutorial
<br>

[![Raspberry Pi Pico W: WiFi  Controlled Robot](https://i.ytimg.com/vi/iTo4Qh2R6m4/maxresdefault.jpg)](https://www.youtube.com/watch?v=iTo4Qh2R6m4 "Raspberry Pi Pico W: WiFi  Controlled Robot")   
 

 3. [link to thonny micropython IDE](https://thonny.org/)

 4. [link to micropython pico W](https://micropython.org/download/RPI_PICO_W/)

 5. [link to reset the pico w](https://github.com/dwelch67/raspberrypi-pico/blob/main/flash_nuke.uf2) <br> hopefully optional

<br>

## The final code used in the video can be downloaded or copy pasted from below as follows: <br>
### 1. Web Control

```
import network
import socket
from time import sleep
import machine

# Yes, these could be in another file. But on the Pico! So no more secure. :)
ssid = 'Your_Network_Name'
password = 'Your_WiFi_Password'

def move_forward():
    print ("Forward")
    
def move_backward():
    print ("Backward")
    
def move_stop():
    print ("Stop")
    
def move_left():
    print ("Left")
    
def move_right():
    print ("Right")
    
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
    
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage():
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>Zumo Robot Control</title>
            </head>
            <center><b>
            <form action="./forward">
            <input type="submit" value="Forward" style="height:120px; width:120px" />
            </form>
            <table><tr>
            <td><form action="./left">
            <input type="submit" value="Left" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./stop">
            <input type="submit" value="Stop" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./right">
            <input type="submit" value="Right" style="height:120px; width:120px" />
            </form></td>
            </tr></table>
            <form action="./back">
            <input type="submit" value="Back" style="height:120px; width:120px" />
            </form>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    #Start web server
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/forward?':
            move_forward()
        elif request =='/left?':
            move_left()
        elif request =='/stop?':
            move_stop()
        elif request =='/right?':
            move_right()
        elif request =='/back?':
            move_backward()
        html = webpage()
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
```
### 2. Motor Test
```
from time import sleep
from machine import Pin

Mot_A_Forward = Pin(18, Pin.OUT)
Mot_A_Back = Pin(19, Pin.OUT)
Mot_B_Forward = Pin(20, Pin.OUT)
Mot_B_Back = Pin(21, Pin.OUT)

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
```
### 3. [Final Code](https://github.com/zacw-243L/Roboto-Project-for-NYP-robotics-CCA/blob/main/Final%20Code.py)
```
import network
import socket
from time import sleep
import machine
from machine import Pin

# Yes, these could be in another file. But on the Pico! So no more secure. :)
ssid = 'Your_Network_Name'
password = 'Your_WiFi_Password'

# Define pins to pin motors!
Mot_A_Forward = Pin(18, Pin.OUT)
Mot_A_Back = Pin(19, Pin.OUT)
Mot_B_Forward = Pin(20, Pin.OUT)
Mot_B_Back = Pin(21, Pin.OUT)

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

#Stop the robot as soon as possible
move_stop()
    
def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        sleep(1)
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
    
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def webpage():
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <head>
            <title>Zumo Robot Control</title>
            </head>
            <center><b>
            <form action="./forward">
            <input type="submit" value="Forward" style="height:120px; width:120px" />
            </form>
            <table><tr>
            <td><form action="./left">
            <input type="submit" value="Left" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./stop">
            <input type="submit" value="Stop" style="height:120px; width:120px" />
            </form></td>
            <td><form action="./right">
            <input type="submit" value="Right" style="height:120px; width:120px" />
            </form></td>
            </tr></table>
            <form action="./back">
            <input type="submit" value="Back" style="height:120px; width:120px" />
            </form>
            </body>
            </html>
            """
    return str(html)

def serve(connection):
    #Start web server
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/forward?':
            move_forward()
        elif request =='/left?':
            move_left()
        elif request =='/stop?':
            move_stop()
        elif request =='/right?':
            move_right()
        elif request =='/back?':
            move_backward()
        html = webpage()
        client.send(html)
        client.close()

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
```
<br>
Be sure to ask the Cher for the password to the wifi <br> (only works locally)<br>
<br>
this might be out of date ...
  
  
  <br>
  
  - ssid = 'DWR-921-F8C5'
  - password = 'eTvwcPX5'

  <br>

#### Cerdit to Christopher Barnatt for providing all the Python code above
<br>

# once you have done all of the above ...
<br>
you should have a working robot that looks like this...
<br>


https://github.com/zacw-243L/Roboto-Project-for-NYP-robotics-CCA/assets/58255472/c843cf3b-05e1-4dd4-ae39-a13bed93fc13

cerdit to me for the video



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
Python code above done by me and roy.

# After some modding and adding new code...
<br>
you should have a working robot that looks like this...
<br>


https://github.com/zacw-243L/Roboto-Project-for-NYP-robotics-CCA/assets/58255472/8891ed82-aafc-4d91-a408-55f4f8501dbf

a working romba that moves in random directions<br>
Cerdit to me fo the video



