from machine import Pin
import time

# Define pins
TRIG_PIN = 16
ECHO_PIN = 17

# Setup pins
trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

def get_distance():
    # Send a 10us pulse to trigger
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    
    # Measure the duration of the echo pulse
    while echo.value() == 0:
        pass
    start = time.ticks_us()
    
    while echo.value() == 1:
        pass
    end = time.ticks_us()
    
    # Calculate distance in cm
    duration = time.ticks_diff(end, start)
    distance = (duration / 2) / 29.1  # Speed of sound is 34300 cm/s
    
    return distance

def read_distance():
    distance = get_distance()
#    print('Distance: {:.2f} cm'.format(distance))
    time.sleep(0.1)
    return distance

