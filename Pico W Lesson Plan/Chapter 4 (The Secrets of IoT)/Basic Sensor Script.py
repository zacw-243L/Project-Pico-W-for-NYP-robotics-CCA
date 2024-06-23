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
