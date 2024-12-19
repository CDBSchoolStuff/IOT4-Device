from machine import Pin, PWM
import time

# Initialize PWM on a specific pin with a higher frequency to reduce noise
pwm = PWM(Pin(4), freq=25000, duty=1000)  # 25 kHz frequency, 50% duty cycle

# Function to control the vibration motor
def vibrate(timer = 0.3):
    pwm.duty(800)  # Set duty cycle 
    time.sleep(timer)
    pwm.duty(0)  # Turn off
    return


vibrate()