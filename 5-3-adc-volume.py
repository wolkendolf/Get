import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

def dec2bin(decimal):
    return [int(i) for i in bin(decimal)[2:].zfill(bits)]

def adc():
    min = 0
    max = 255
    while (max - min) > 1:
        middle = (max + min) // 2
        GPIO.output(dac, dec2bin(int(middle)))
        time.sleep(0.007)
        if GPIO.input(comp) == 0:
            max = middle
        else:
            min = middle
    return min

dac = [26, 19, 13, 6, 5, 11, 9, 10]
leds = [24, 25, 8, 7, 12, 16, 20, 21]
comp = 4
troyka = 17

GPIO.setup(dac, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(dac, GPIO.OUT, initial=GPIO.HIGH)
GPIO.setup(leds, GPIO.OUT)

bits = len(dac)
levels = 2**bits
max_v = 3.3

try:
    while True:
        v = adc()
        print(v)
        voltage = v / levels * max_v
        signal = dec2bin(v)
        n = int(round(v/(60/8)))
        n = min(8, n)
        GPIO.output(leds, [1]*n + [0]*(8-n))
        print(voltage, signal)
finally:
    GPIO.output(dac, 0)
    GPIO.output(troyka, 0)
    GPIO.cleanup()
