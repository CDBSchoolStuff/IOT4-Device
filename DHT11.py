from machine import Pin
import time
#DHT library
import dht



#Defines DHT data pin to ESP32
DHTPin = 19
# Instantiates sensor object to use DHT11
sensor = dht.DHT11(Pin(DHTPin))  

#Function for simple temperature reading
def DHT11_READ():
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        return temp,hum
#Incase of no read value due to error, ignore this attempt and continue
    except OSError as e:
        print("Failed to read sensor.")
