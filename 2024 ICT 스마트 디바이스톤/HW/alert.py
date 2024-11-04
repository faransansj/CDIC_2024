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
from collections import Counter

# pin map
tilt_switch = 4

boozer = 14
led_Rsig = 15
led_Gsig = 17
led_Bsig = 27
led_gnd = 18

parking = 1

# setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(tilt_switch, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(boozer, GPIO.OUT)

GPIO.setup(led_Rsig, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_Gsig, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_Bsig, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(led_gnd, GPIO.OUT, initial=GPIO.LOW)

# melody data - you can change other music feel free! :)
notes_parkO = "egcefg"
beats_parkO = [1, 1, 1, 1, 1, 1]
tempo_parkO = 100

notes_parkX = "ececec"
beats_parkX = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
tempo_parkX = 140

notes_tilt = "fcfcfc"
beats_tilt = [1, 1, 0.5, 1, 1, 0.5]
tempo_tilt = 90

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

def play_buzzer_parkO_pattern():
    for i in range(len(notes_parkO)):
        if notes_parkO[i] == ' ':
            time.sleep(beats_parkO[i] * tempo_parkO / 1000.0)
        else:
            play_note(notes_parkO[i], beats_parkO[i] * tempo_parkO)
        time.sleep(tempo_parkO / 10000.0)

def play_buzzer_parkX_pattern():
    for i in range(len(notes_parkX)):
        if notes_parkX[i] == ' ':
            time.sleep(beats_parkX[i] * tempo_parkX / 1000.0)
        else:
            play_note(notes_parkX[i], beats_parkX[i] * tempo_parkX)
        time.sleep(tempo_parkX / 10000.0)

def play_buzzer_tilt_pattern():
    for i in range(len(notes_tilt)):
        if notes_tilt[i] == ' ':
            time.sleep(beats_tilt[i] * tempo_tilt / 1000.0)
        else:
            play_note(notes_tilt[i], beats_tilt[i] * tempo_tilt)
        time.sleep(tempo_tilt / 10000.0)

def alert_park(input_sig):
    # 0 = park O | 1 = park X 
    if input_sig == 0:
        print("park O")
        GPIO.output(led_Rsig, 0)
        GPIO.output(led_Gsig, 1)
        GPIO.output(led_Bsig, 0)
        GPIO.output(led_gnd, 0)
        play_buzzer_parkO_pattern()
    else:
        print("park X")
        GPIO.output(led_Rsig, 0)
        GPIO.output(led_Gsig, 0)
        GPIO.output(led_Bsig, 1)
        GPIO.output(led_gnd, 0)
        play_buzzer_parkX_pattern()

def read_tilt_switch(samples=10):
    readings = []
    for _ in range(samples):
        readings.append(GPIO.input(tilt_switch))
        time.sleep(0.01)  # 짧은 대기 시간으로 여러 번 샘플링
    most_common_value = Counter(readings).most_common(1)[0][0]
    return most_common_value

def alert_tilt():
    print("kickboard tilted!!!")
    GPIO.output(led_Rsig, 1)
    GPIO.output(led_Gsig, 0)
    GPIO.output(led_Bsig, 0)
    GPIO.output(led_gnd, 0)
    play_buzzer_tilt_pattern()

if __name__ == "__main__":
    try:
        while True:
            tilt_status = read_tilt_switch()
            if tilt_status == GPIO.LOW:
                print("tilt o")
                alert_tilt()        
                time.sleep(0.5)
                continue
            else:
                print("tilt x")
            
            if parking == 1:
                alert_park(0)
            else:
                alert_park(1)
                    
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("good bye")
        
    finally:
        GPIO.cleanup()