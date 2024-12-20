from machine import ADC, Pin, Timer
import time
import buzzer as play
import math
mic = ADC(Pin(33))
ldr = ADC(Pin(35))
switch = Pin(27, Pin.OUT)
switch.value(0)
# Turn on microphone 
# Allows voltages between 0.0V to 3.3V
mic.atten(ADC.ATTN_11DB)
on_off = 1

# Set the ADC width (resolution) to 12 bits (0-4095)
mic.width(ADC.WIDTH_12BIT)

# Allows voltages between 0.0V to 3.3V
ldr.atten(ADC.ATTN_11DB)
# Set the ADC width (resolution) to 12 bits (0-4095)
ldr.width(ADC.WIDTH_12BIT)

def microphone_on_off():
    global on_off
    if on_off == 1:
        switch.value(1)
        on_off = 0
        play.success_melody()
        print("Microphone on!")
        return on_off
    else:
        switch.value(0)
        on_off = 1
        play.failure_melody()
        print("Microphone off!")
        return on_off




# Reads the two different ADC pins and returns the values
def read_adc():
	mic_val = mic.read()
	ldr_val = ldr.read()
	time.sleep(0.1)
	return mic_val,ldr_val

# Function to calculate average between latest 10 readings of the microphone
def average_readings():
    # Creates tuple to fill with latest 10 readings
    readings = []
    for _ in range(10):
        reading = mic.read()
        readings.append(reading)
        # Small delay between readings
        time.sleep(0.1)

    average = sum(readings) / len(readings)
    return average


# Function to read and process light sensor data
def read_lux():
    analog_value = ldr.read()  # Read the raw ADC value
    voltage = analog_value * (3.3 / 4095.0)  # Convert ADC value to voltage (assuming 3.3V max)
    lux = analog_value * (198 / 2200.0)  # Calculate lux using the calibrated factor

    #print(f"Analog Value = {analog_value} Voltage = {voltage:.3f} Lux = {lux:.2f}")
    return round(lux, 2)



# Function to convert ADC value to decibels (dB)
def adc_to_db():
    adc_val = mic.read()

    if adc_val == 0.0:
        return 0.0
    
    return 20 * math.log10(adc_val/4095)