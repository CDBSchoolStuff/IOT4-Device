############################
#Imports
import testboot
import time 
import ultrasonic_sensor as us
import vibrationmotor as vib
import DHT11 as weather
import WS2812B as LED
import ADC as micldr
import buzzer as play
import credentials

###########################
#Global variables
global ldr_val
global avg

###########################
#Variables for later use
temp_passed = 0
hum_passed = 0
light_passed = 0
mic_passed = 0


#############
#Temperature and Humidity check
def temp_hum_check(timer = 0.5):
    global temp_passed
    global hum_passed
    if 19 < temp < 22:
        LED.fade_color(LED.last_color , ( 0, 80 , 0) )
        print("Just right.")
        temp_passed = 1
        play.success_melody()
    elif temp < 19:
        LED.fade_color(LED.last_color , ( 0, 0 , 80) )
        print(temp)
        print("Too cold!")
        temp_passed = 0
    else:
        LED.fade_color(LED.last_color , ( 80, 0 , 0) )
        print("Too warm!")
        temp_passed = 0
    LED.fade_color_flash()
    time.sleep(timer)
    
    
    if 30 < hum < 50:
        LED.fade_color(LED.last_color , ( 0, 80 , 0) )
        print("Just right.")
        hum_passed = 1
        play.success_melody()
    elif hum < 30:
        LED.fade_color(LED.last_color , ( 80 , 0 ,  0) )
        print(hum)
        print("Too dry!")
        hum_passed = 0
    else:
        LED.fade_color(LED.last_color , ( 0 , 0 , 80) )
        print(hum)
        print("Too humid!")
        hum_passed = 0
    time.sleep(timer)
###############################
#Second function for dark mode of above checks (Less bright.)
def temp_hum_check_dark(timer = 0.5):
    global temp_passed
    global hum_passed
    if 19 < temp < 22:
        LED.fade_color(LED.last_color , ( 0, 20 , 0) )
        print("Just right.")
        temp_passed = 1
        play.success_melody()
    elif temp < 19:
        LED.fade_color(LED.last_color , ( 0, 0 , 20) )
        print(temp)
        print("Too cold!")
        temp_passed = 0
    else:
        LED.fade_color(LED.last_color , ( 20, 0 , 0) )
        print("Too warm!")
        temp_passed = 0
    LED.fade_color_flash((20,4,0))
    time.sleep(timer)
    
    if 30 < hum < 50:
        LED.fade_color(LED.last_color , ( 0, 20 , 0) )
        print("Humidity is good!")
        hum_passed = 1
        play.success_melody()
    elif hum < 30:
        LED.fade_color(LED.last_color , ( 20 , 0 ,  0) )
        print("Too dry!")
        hum_passed = 0
    else:
        LED.fade_color(LED.last_color , ( 0 , 0 , 20) )
        print(hum)
        print("Too humid!")
        hum_passed = 0
    time.sleep(timer)
    

#################################
#Checks light and mic ADC values
def light_mic_check(timer = 0.5):
    global light_passed
    global mic_passed
    mic_val, ldr_val = micldr.read_adc()
    if ldr_val < 200:
        print("Optimal light level!")
        LED.fade_color_flash((0,0,20))
        LED.fade_color_flash((0,0,20))
        light_passed = 1
        return light_passed
    else:
        print("Lower the light level for optimal sleep!")
        LED.fade_color(LED.last_color , ( 80 , 80 , 80) )
        light_passed = 0
        pass
    if avg <= 200 and micldr.on_off == 0:
        print(f"Current average mic level: {avg}")
        mic_passed = 1
    else:
        print(f"Current average mic level: {avg}")
        mic_passed = 0
    time.sleep(timer)
    
##################################
#To check for perfect sleep conditions
def sleep_condition():
    print(light_passed,light_passed,temp_passed,hum_passed)
    number_satisfied = 0 + light_passed + temp_passed + hum_passed + mic_passed
    print(f"Total satisfaction:{number_satisfied} out of 4")
    if number_satisfied == 4 and on_off == 1:
        play.success_melody
        vib.vibrate()
        sleep(0.5)
        vib.vibrate()
        print("Perfect condition!")
    elif number_satisfied == 3 and on_off == 0:
        play.success_melody
        vib.vibrate()
        sleep(0.5)
        vib.vibrate()
        print("Perfect condition, sound not measured!")
    else:
        play.failure_melody()
        print("Conditions for a good sleep not met.")
        
##########################
#Unpacking / creating the variables for startup use
mic_val, ldr_val = micldr.read_adc()


#########################
#Main loop, uses the different features on the board for sleep condition monitoring
try:
    micldr.microphone_on_off()
    while True:
        # Unpacking / creating temp and hum variables for use in functions
        temp, hum = weather.DHT11_READ()
        # Takes the avg of 10 readings from the adctest.py file for use in sound monitoring
        avg = micldr.average_readings()
        # If too bright, use bright LED
        if ldr_val > 200: 
            LED.fade_color(LED.last_color , (120, 100 ,0) )
            bright = True
            # If too dark, use weaker values to avoid waking user
        else: 
            LED.fade_color(LED.last_color , (30, 16 ,0) )
            bright = False
# For interacting with unit, 15 cm or under solution to trigger in darkmode
#Runs checks on different features and displays status using colored LED.
        if 35 < us.read_distance() < 50:
            global on_off
            on_off = micldr.microphone_on_off()
            print(on_off)
            time.sleep(1)
            


        if 0 < us.read_distance() < 15 and bright == False: 
            vib.vibrate()
            print("Low light level!")
            previous_color = LED.last_color
            LED.fade_color(LED.last_color , (20, 4 ,0) )
            temp_hum_check_dark()
            LED.fade_color_flash((20,4,0))
            light_mic_check()
            LED.fade_color(LED.last_color , previous_color )
            sleep_condition()

 # For interacting with unit, 15 cm or under solution to trigger in bright mode
 #Runs checks on different features and displays status using colored LED.
        elif 0 < us.read_distance() < 15:
            print("Bright light level!")
            vib.vibrate()
            previous_color = LED.last_color
            LED.fade_color(LED.last_color , (160, 40 ,0) )
            temp_hum_check()
            LED.fade_color_flash()
            light_mic_check()
            LED.fade_color_flash()
            LED.fade_color(LED.last_color , previous_color )
            sleep_condition()
            
            # If not under 15cm, repeat loop
        else:
            pass
        #To allow escape from Loop incase of bad code
except KeyboardInterrupt:
    play.failure_melody()
    LED.fade_color(LED.last_color , (0, 0 ,0) )
    print("Exiting loop. Good day!")
    
    
        
        
        
        
        
    





