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
