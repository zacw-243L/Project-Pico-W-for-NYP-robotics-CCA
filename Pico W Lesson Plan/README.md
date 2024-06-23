# Pico W Lesson Plan for NYP robotics CCA
<br>

# Chapter 3: Your First Program
<br>

## [Blink.py](https://github.com/zacw-243L/Project-Pico-W-for-NYP-robotics-CCA/blob/Master-Repo/Pico%20W%20Lesson%20Plan/Blink.py)<br>

Enter the following code to toggle the LED.

```
import machine
led = machine.Pin("LED", machine.Pin.OUT)
led.toggle()
```

## [Blinker.py](https://github.com/zacw-243L/Project-Pico-W-for-NYP-robotics-CCA/blob/Master-Repo/Pico%20W%20Lesson%20Plan/Blinker.py)<br>

You can use the Timer module to set a timer that runs a function at regular intervals. Update your code so it looks like this:

```
import machine
from machine import Timer

led = machine.Pin("LED", machine.Pin.OUT)
timer = Timer()

def blink(timer):
    led.toggle()

timer.init(freq=2.5, mode=Timer.PERIODIC, callback=blink)
```

# Chapter 3.2: Connecting to the Internet<br>

## [Connecting to the Internet.py](https://github.com/zacw-243L/Project-Pico-W-for-NYP-robotics-CCA/blob/Master-Repo/Pico%20W%20Lesson%20Plan/Chapter%203.2%20(Connecting%20to%20the%20Internet)/Connecting%20to%20the%20Internet.py)<br>

There are many ways to connect a PIco W to the internet. One of the ways includes running an HTML file inside a Python script.<br>
(the files inside the folder Chapter 3.2 (Connecting to the Internet) can be directly uploaded to your Pico W)


```
import network
import socket
from time import sleep
from picozero import pico_temp_sensor, pico_led
import machine

ssid = ''
password = ''


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


def webpage(temperature, state):
    #Template HTML
    html = f"""
            <!DOCTYPE html>
            <html>
            <form action="./lighton">
            <input type="submit" value="Light on" />
            </form>
            <form action="./lightoff">
            <input type="submit" value="Light off" />
            </form>
            <p>LED is {state}</p>
            <p>Temperature is {temperature}</p>
            </body>
            </html>
            """
    return str(html)


def serve(connection):
    #Start a web server
    state = 'OFF'
    pico_led.off()
    temperature = 0
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        try:
            request = request.split()[1]
        except IndexError:
            pass
        if request == '/lighton?':
            pico_led.on()
            state = 'ON'
        elif request =='/lightoff?':
            pico_led.off()
            state = 'OFF'
        temperature = pico_temp_sensor.temp
        html = webpage(temperature, state)
        client.send(html)
        client.close()
        

try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection)
except KeyboardInterrupt:
    machine.reset()
```

# [Chapter 4: The Secrets of IoT](https://github.com/zacw-243L/Project-Pico-W-for-NYP-robotics-CCA/tree/Master-Repo/Pico%20W%20Lesson%20Plan/Chapter%204%20(The%20Secrets%20of%20IoT))<br>

This chapter will teach you about DHT Sensors and how to use the internet to send stuff to the cloud