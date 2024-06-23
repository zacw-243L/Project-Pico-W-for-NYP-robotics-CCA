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

# Chapter 4: A New Sensor<br>

This chapter will teach you about DHT Sensors and how to use the internet to send stuff to the cloud

## [Basic Sensor Script.py](https://github.com/zacw-243L/Project-Pico-W-for-NYP-robotics-CCA/blob/Master-Repo/Pico%20W%20Lesson%20Plan/Chapter%204%20(A%20New%20Sensor)/Basic%20Sensor%20Script.py)<br>

The MicroPython script reads temperature and  humidity readings from the DHT11 sensor. <br>
These readings will be printed on the  MicroPython shell console<br>
(the files inside the folder Chapter 4 (A New Sensor) can be directly uploaded to your Pico W)


```
import machine
import dht
from machine import Pin
from time import sleep

sensor = dht.DHT11(Pin(4))  
led = machine.Pin("LED", machine.Pin.OUT)

while True:
    sleep(0.1)
    sensor.measure()
    temp = sensor.temperature()
    hum = sensor.humidity()
    print("Temperature: {}°C Humidity: {}% ".format(temp, hum))
    
    if hum > 80:
        led.on()
    else:
        led.off()
    
    sleep(1)
```

### Output: 
![osur2](https://github.com/zacw-243L/Project-Pico-W-for-NYP-robotics-CCA/assets/58255472/e7977912-fcdc-42e7-bc4d-d9293a9119eb)

# Chapter 4.1: The Secrets of IoT<br>

IoT Data Analytics and Visualization. You will need an Adafruit io account from now on. <br>
If you do not have an account [click here](https://accounts.adafruit.com/users/sign_up) to sign up for one<br>
Once you have signed up, you can start using the code below.<br>
(the files inside the folder Chapter 4.1 (The Secrets of IoT) can be directly uploaded to your Pico W)

## [Sending Data Only.py](https://github.com/zacw-243L/Project-Pico-W-for-NYP-robotics-CCA/blob/Master-Repo/Pico%20W%20Lesson%20Plan/Chapter%204.1%20(The%20Secrets%20of%20IoT)/Sending%20Data%20Only.py)

```
from machine import Pin
from time import sleep
from machine import Timer
from umqtt.simple import MQTTClient
import dht
import network
import time
import sys

sensor = dht.DHT11(Pin(4))

ssid = ''
password = ''
mqtt_client_id = bytes('client_'+'12321', 'utf-8') # Just a random client ID

ADAFRUIT_IO_URL = 'io.adafruit.com'
ADAFRUIT_USERNAME = 'Studentwastaken'
ADAFRUIT_IO_KEY = ''

TEMP_FEED_ID = 'cca-temperature'
HUM_FEED_ID = 'cca-humidity'


def connect_wifi():
    wifi = network.WLAN (network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(ssid, password)
    if not wifi.isconnected():
        print('Connecting..')
        timeout = 0
        while (not wifi.isconnected() and timeout < 5):
            print(5 - timeout)
            timeout = timeout + 1
            time.sleep(1)
    if(wifi.isconnected()):
        print('Connected!')
    else:
        print('Not Connected!')
        sys.exit()
        
connect_wifi()
client = MQTTClient(client_id=mqtt_client_id, server=ADAFRUIT_IO_URL, user=ADAFRUIT_USERNAME, password=ADAFRUIT_IO_KEY, ssl=False)

try:
    client.connect()
except Exception as e:
    print('Could not connect to MQTT server {}{}'.format(type (e)._name,e))
    sys.exit()
    
temp_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TEMP_FEED_ID), 'utf-8') # format techiesms/feeds/temp
hum_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, HUM_FEED_ID), 'utf-8') # format techiesms/feeds/hum


def sens_data(data):
    sensor.measure()
    temp = sensor.temperature() # Measuring
    hum = sensor.humidity() #getting Temp
    client.publish(temp_feed, bytes(str(temp), 'utf-8'), qos=0) # Publishing Temp feed to adafruit.io
    client.publish(hum_feed, bytes (str(hum), 'utf-8'), qos=0) #Publishing Hum feed to adafruit.io
    print("Temperature: ", str(temp))
    print("Humidity: ", str(hum))
    print('')
    
timer = Timer(-1)
timer.init(period=5000, mode = Timer.PERIODIC, callback = sens_data)
```

# Chapter 4.2: Sending and Receiving <br>

To read data from the cloud, we could use either HTTP API or MQTT API. <br>
To achieve this with Adafruit.io, we will create a  new Micropython code.<br>
This will allow us to control the Raspberry Pi Pico W onboard LED using the cloud toggle switch.<br>

(the files inside the folder Chapter 4.2 (Sending and Receiving) can be directly uploaded to your Pico W)

## [A 2 way road.py](https://github.com/zacw-243L/Project-Pico-W-for-NYP-robotics-CCA/blob/Master-Repo/Pico%20W%20Lesson%20Plan/Chapter%204.2%20(Sending%20and%20Receiving)/A%202%20way%20road.py)<br>

```
from machine import Pin
from time import sleep
from machine import Timer
from umqtt.simple import MQTTClient
import dht
import network
import time
import sys

led = Pin('LED', Pin.OUT)
sensor = dht.DHT11(Pin(4))

ssid = ''
password = ''

mqtt_client_id = bytes('client_' + '12321', 'utf-8')  # Just a random client ID

ADAFRUIT_IO_URL = 'io.adafruit.com'
ADAFRUIT_USERNAME = 'Studentwastaken'
ADAFRUIT_IO_KEY = ''

TOGGLE_FEED_ID = 'cca-led'
TEMP_FEED_ID = 'cca-temperature'
HUM_FEED_ID = 'cca-humidity'


def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(ssid, password)
    if not wifi.isconnected():
        print('Connecting..')
        timeout = 0
        while (not wifi.isconnected() and timeout < 5):
            print(5 - timeout)
            timeout = timeout + 1
            time.sleep(1)
    if (wifi.isconnected()):
        print('Connected!')
    else:
        print('Not Connected!')
        sys.exit()


connect_wifi()
client = MQTTClient(client_id=mqtt_client_id, server=ADAFRUIT_IO_URL, user=ADAFRUIT_USERNAME, password=ADAFRUIT_IO_KEY,
                    ssl=False)

try:
    client.connect()
except Exception as e:
    print('Could not connect to MQTT server {}{}'.format(type(e)._name, e))
    sys.exit()

toggle_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID), 'utf-8')
temp_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TEMP_FEED_ID), 'utf-8')  # format techiesms/feeds/temp
hum_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, HUM_FEED_ID), 'utf-8')  # format techiesms/feeds/hum


def cb(topic, msg):  # callback function
    print('Received Data: Topic = {}, Msg = {}'.format(topic, msg))
    received_data = str(msg, 'utf-8')  # Receiving data
    if received_data == "ON":
        led.on()
    if received_data == "OFF":
        led.off()


def sens_data(data):
    sensor.measure()
    temp = sensor.temperature()  # Measuring
    hum = sensor.humidity()  # getting Temp
    client.publish(temp_feed, bytes(str(temp), 'utf-8'), qos=0)  # Publishing Temp feed to adafruit.io
    client.publish(hum_feed, bytes(str(hum), 'utf-8'), qos=0)  # Publishing Hum feed to adafruit.io
    print("Temperature: ", str(temp))
    print("Humidity: ", str(hum))
    print('')


client.set_callback(cb)  # callback function
client.subscribe(toggle_feed)  # subscribing to particular topic
timer = Timer(-1)
timer.init(period=5000, mode=Timer.PERIODIC, callback=sens_data)

while True:
    try:
        client.check_msg()  # non blocking function
    except:
        client.disconnect()
        sys.exit()
```

# Chapter 4.3: Control Device from Cloud<br>

## Activity: Control Device from Cloud<br>

Time to apply what you have learnt.<br>
Control the Raspberry Pi Pico W LED.<br>
Set the LED to 1 if the humidity is more than 80, else  set the LED to 0.<br>

<details>
  <summary>Answers</summary>

  <br>
  
  Answers for those who cannot figure it out in time. <br>

  (the files inside the folder Chapter 4.3 (Control Device from Cloud) (Activity) can be directly uploaded to your Pico W)

  ## [Answers.py](https://github.com/zacw-243L/Project-Pico-W-for-NYP-robotics-CCA/blob/Master-Repo/Pico%20W%20Lesson%20Plan/Chapter%204.3%20(Control%20Device%20from%20Cloud)%20(Activity)/Answers.py)<br>

  ```
from machine import Pin
from time import sleep
from machine import Timer
from umqtt.simple import MQTTClient
import dht
import network
import time
import sys

led = Pin('LED', Pin.OUT)
sensor = dht.DHT11(Pin(4))

ssid = ''
password = ''

mqtt_client_id = bytes('client_' + '12321', 'utf-8')  # Just a random client ID

ADAFRUIT_IO_URL = 'io.adafruit.com'
ADAFRUIT_USERNAME = 'Studentwastaken'
ADAFRUIT_IO_KEY = ''

TOGGLE_FEED_ID = 'cca-led'
TEMP_FEED_ID = 'cca-temperature'
HUM_FEED_ID = 'cca-humidity'


def connect_wifi():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.disconnect()
    wifi.connect(ssid, password)
    if not wifi.isconnected():
        print('Connecting..')
        timeout = 0
        while (not wifi.isconnected() and timeout < 5):
            print(5 - timeout)
            timeout = timeout + 1
            time.sleep(1)
    if (wifi.isconnected()):
        print('Connected!')
    else:
        print('Not Connected!')
        sys.exit()


connect_wifi()
client = MQTTClient(client_id=mqtt_client_id, server=ADAFRUIT_IO_URL, user=ADAFRUIT_USERNAME, password=ADAFRUIT_IO_KEY,
                    ssl=False)

try:
    client.connect()
except Exception as e:
    print('Could not connect to MQTT server {}{}'.format(type(e)._name, e))
    sys.exit()

toggle_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TOGGLE_FEED_ID), 'utf-8')
temp_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, TEMP_FEED_ID), 'utf-8')  # format techiesms/feeds/temp
hum_feed = bytes('{:s}/feeds/{:s}'.format(ADAFRUIT_USERNAME, HUM_FEED_ID), 'utf-8')  # format techiesms/feeds/hum


def cb(topic, msg):  # callback function
    print('Received Data: Topic = {}, Msg = {}'.format(topic, msg))
    received_data = str(msg, 'utf-8')  # Receiving data
    if received_data == "ON":
        led.on()
    if received_data == "OFF":
        led.off()


def CBH(topic, msg):
    print('Received Data: Topic = {}, Msg = {}'.format(topic, msg))
    received_data = int(str(msg, 'utf-8'))  # Receiving data
    if received_data > 80:
        led.on()
    else:
        led.off()


def sens_data(data):
    sensor.measure()
    temp = sensor.temperature()  # Measuring
    hum = sensor.humidity()  # getting Temp
    client.publish(temp_feed, bytes(str(temp), 'utf-8'), qos=0)  # Publishing Temp feed to adafruit.io
    client.publish(hum_feed, bytes(str(hum), 'utf-8'), qos=0)  # Publishing Hum feed to adafruit.io
    print("Temperature: ", str(temp))
    print("Humidity: ", str(hum))
    print('')


client.set_callback(cb)  # callback function
client.subscribe(toggle_feed)  # subscribing to particular topic
client.set_callback(CBH)  # callback function
client.subscribe(hum_feed)  # Subscribe to the topic
timer = Timer(-1)
timer.init(period=5000, mode=Timer.PERIODIC, callback=sens_data)

while True:
    try:
        client.check_msg()  # non blocking function
    except:
        client.disconnect()
        sys.exit()
  ```

  
</details>


