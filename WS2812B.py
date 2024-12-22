import time
from machine import Pin
#Imports NeoPixel library
import neopixel

# Variables to easily change number of LED's and which Pin 
n = 1  # Number of LEDs in the strip
p = 22  # GPIO pin connected to the NeoPixel strip
# Initialize NeoPixel object
np = neopixel.NeoPixel(Pin(p), n)

#Function to seamlessly fade from starting color to end color, with definable colors, steps and delay between steps
def fade_color(start_color, end_color, steps=15, delay=0.10,):
	#This is global, to let function acquire latest used end color 
	global last_color
	for step in range(steps + 1):
		r = start_color[0] + (end_color[0] - start_color[0]) * step // steps
		g = start_color[1] + (end_color[1] - start_color[1]) * step // steps
		b = start_color[2] + (end_color[2] - start_color[2]) * step // steps
		for i in range(n):
			np[i] = (r, g, b)
		np.write()
		last_color = end_color
		time.sleep(delay)
	#last_color becomes the latest end_color, to let programmer only have to define the new end_color if they wish.
	last_color = end_color
	return last_color

# Function to flash a color when used in the program
# Used for signaling "loading" or "transitioning" for end user
def fade_color_flash(base_color = (140,40,0)):
    fade_color(last_color , ( 0, 0 , 0) )
    fade_color(last_color , ( base_color))

        
# Not used, but allows static color without color fading / blending
# Function to set all LEDs to a specific color
def set_color(r, g, b):
    for i in range(n):
        np[i] = (r, g, b)
    np.write()
    
