from machine import Pin, PWM
from time import sleep

# Creates object Buzzer with PWM on Pin 21
buzzer = PWM(Pin(21))

# Different frequencies to allow melodies, each frequency responds to a note
C5 = 523
E5 = 659
G5 = 784
C6 = 1047
A4 = 440
F4 = 349
D4 = 294
C4 = 262
E4 = 330
G4 = 392
B4 = 494

# Function to play specific note / tone
def play_tone(frequency, duration):
    buzzer.freq(frequency)
    # 25% duty cycle to reduce volume
    buzzer.duty(256) 
    sleep(duration)
    buzzer.duty(0)
    #Delay between notes
    sleep(0.05)  

# Function for a melody indicating success
# Melody is built from Tuple indicating the note ( which is a specific frequency seen above),
#and the amount of time it is played. Sequence of the tuple decides the order
def success_melody():
    melody = [
        (C5, 0.05), (E5, 0.05), (G5, 0.05), (C6, 0.3)
    ]
    for note, duration in melody:
        play_tone(note, duration)
        
def failure_melody():
    melody = [
        (C5, 0.05), (A4, 0.05), (F4, 0.05), (D4, 0.3)
    ]
    for note, duration in melody:
        play_tone(note, duration)
        
def init_melody():
    melody = [
        (C4, 0.2), (E4, 0.2), (G4, 0.2), (C5, 0.4),
        (G4, 0.2), (E4, 0.2), (C4, 0.2), (D4, 0.2),
        (F4, 0.2), (A4, 0.2), (C5, 0.4), (B4, 0.2),
        (G4, 0.2), (E4, 0.2), (C4, 0.4)
    ]
    for note, duration in melody:
        play_tone(note, duration)




        