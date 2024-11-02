'''######################################################################
# alert.py                                                              #
# this library using for alert LED, Buzzer                              #
# setup : you can change pin map tilt,buzzer,led                        #
# led_gnd is definde you must this pin altime make GPIO.LOW             #
#                                                                       #
# alert.play_buzzer_pattern() : play melody one time                    #
# alert(input_sig) : input_sig = 0 no alert / input_sif = 1 alert on    #
######################################################################'''

import RPi.GPIO as GPIO
import time

# pin map
tilt_switch = 4
boozer = 14
led_sig = 15
led_gnd = 18

# setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(tilt_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(boozer, GPIO.OUT)
GPIO.setup(led_sig, GPIO.OUT)
GPIO.setup(led_gnd, GPIO.OUT)

# melody data - you can change other music feel free! :)
notes = "egcefg"
beats = [1, 1, 1, 1, 1, 1]
tempo = 100

def play_tone(tone, duration):
    for i in range(int(duration * 1000 / (tone * 2))):
        GPIO.output(boozer, GPIO.HIGH)
        time.sleep(tone / 1000000.0)
        GPIO.output(boozer, GPIO.LOW)
        time.sleep(tone / 1000000.0)

def play_note(note, duration):
    names = ['c', 'd', 'e', 'f', 'g', 'a', 'b', 'C']
    tones = [1915, 1700, 1519, 1432, 1275, 1136, 1014, 956]
    if note in names:
        tone = tones[names.index(note)]
        play_tone(tone, duration)

def play_buzzer_pattern():
    for i in range(len(notes)):
        if notes[i] == ' ':
            time.sleep(beats[i] * tempo / 1000.0)
        else:
            play_note(notes[i], beats[i] * tempo)
        time.sleep(tempo / 10000.0)

def alert(input_sig):
    if input_sig == 0:
        print("tilt off")
        GPIO.output(led_sig, 0)
        GPIO.output(led_gnd, 0)
    else:
        print("tilt on")
        GPIO.output(led_sig, 1)
        GPIO.output(led_gnd, 0)
        play_buzzer_pattern()

if __name__ == "__main__":
    try:
        play_buzzer_pattern()
        while True:
            if GPIO.input(tilt_switch) == GPIO.LOW:
                print("tilt off")
                alert(0)
            else:
                print("tilt on")
                alert(1)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("good bye")
    finally:
        GPIO.cleanup()
