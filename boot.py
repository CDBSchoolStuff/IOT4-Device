print("Booting.")
from time import ticks_ms, sleep
sleep(2) # Pausing code before running anything to prevent bad code from causing boot looping.

from credentials import credentials
import WS2812B as LED
import buzzer as play
import network
import esp
import logging


#####
#MQTT
from umqttsimple import MQTTClient

# MQTT
MQTT_TOPIC_SENSORDATA = 'mqtt_sensordata'
MQTT_CHECK_CONNECTION_DELAY = 10
COMPLETE_TIMEOUT = 1200000

mqtt_server = credentials['mqtt_server']
client_id = credentials['client_id']
last_message = 0
message_interval = 5


def connect_and_subscribe(topic_sub):
  global client_id, mqtt_server
  
  mqtt_client = MQTTClient(client_id, mqtt_server)
  mqtt_client.connect()
  mqtt_client.subscribe(topic_sub)
  print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
  return mqtt_client


#Audio indication of startup of system
play.init_melody()    

#Visual indication of startup of system
LED.fade_color( (0, 0, 0), (0, 0, 100))  # Red to Blue

sleep(0.5)


#########################################################################
# WIFI CONNECTIVITY

ssid = credentials["ssid"]
password = credentials["password"]

station = network.WLAN(network.STA_IF)

#Attempt to connect to Wi-Fi.
# Success or failure is indicated with LED color, audio.
try:
    print("Starting connection attempt!")
    LED.fade_color( LED.last_color , (160, 50, 0 ), 15 , 0.10)
    sleep(1)
    station.active(True)
    station.connect(ssid, password)

    while station.isconnected() == False:
        pass
    
    print(station.ifconfig())
    print("Connection successful")
    LED.fade_color(LED.last_color, (0, 160, 0 ), 15 , 0.10)
    play.success_melody()
    
    
except: # Incase network doesn't connect, the program allows continuing.
    print("Network connection failed.")
    play.failure_melody()
    LED.fade_color( LED.last_color , (160, 0, 0 ), 15 , 0.10)
    sleep(2)
    

try:
    print("Connecting to MQTT broker!")
    LED.fade_color( LED.last_color , (160, 50, 0 ), 15 , 0.10)
    sleep(1)
    connect_and_subscribe(MQTT_TOPIC_SENSORDATA = 'mqtt_sensordata')
    print("Connection successful")
    LED.fade_color(LED.last_color, (0, 160, 0 ), 15 , 0.10)
    play.success_melody()
    
except: # Incase network doesn't connect, the program allows continuing.
    print("Failed to connect to MQTT broker.")
    play.failure_melody()
    LED.fade_color( LED.last_color , (160, 0, 0 ), 15 , 0.10)
    sleep(2)