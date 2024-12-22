from machine import ADC, Pin, Timer
import time
import math
import buzzer as play

mic = ADC(Pin(33))
ldr = ADC(Pin(35))
switch = Pin(27, Pin.OUT)
switch.value(0)

# Turn on microphone 
mic.atten(ADC.ATTN_6DB)
mic.width(ADC.WIDTH_12BIT)

ldr.atten(ADC.ATTN_11DB)
ldr.width(ADC.WIDTH_12BIT)

on_off = 0

def microphone_on_off():
    global on_off
    if on_off == 0:
        switch.value(1)
        on_off = 1
        print("Microphone on!")
        play.success_melody()
    else:
        switch.value(0)
        on_off = 0
        print("Microphone off!")
        play.failure_melody()
    return on_off

def read_adc():
    mic_val = mic.read()
    ldr_val = ldr.read()
    time.sleep(0.1)
    return mic_val, ldr_val

def average_readings():
    readings = []
    for _ in range(10):
        reading = mic.read()
        readings.append(reading)
        time.sleep(0.1)
    average = sum(readings) / len(readings)
    return average

def read_lux():
    analog_value = ldr.read()  # Read the raw ADC value
    voltage = analog_value * (3.3 / 4095.0)  # Convert ADC value to voltage (assuming 3.3V max)
    lux = analog_value * (198 / 2200.0)  # Calculate lux using the calibrated factor
    return round(lux, 2)

def calculate_rms(samples):
    sum_squares = sum([sample**2 for sample in samples])
    mean_squares = sum_squares / len(samples)
    return math.sqrt(mean_squares)

def adc_to_db():
    samples = [mic.read() for _ in range(1000)]
    rms_voltage = calculate_rms(samples)
    
    if rms_voltage == 0.0:
        return 0.0
    
    sensitivity = -42  # Microphone sensitivity in dBV/Pa
    gain = 10  # Amplifier gain in dB
    reference_voltage = 0.107  # Reference voltage for 0 dB
    
    db = 20 * math.log10(rms_voltage / reference_voltage) + sensitivity + gain
    return db

