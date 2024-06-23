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