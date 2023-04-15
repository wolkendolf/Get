import RPi.GPIO as GPIO
import time

dac = [26, 19, 13, 6, 5, 11, 9, 10]
comp = 4
troyka = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(dac, GPIO.OUT)
GPIO.setup(comp, GPIO.IN)
GPIO.setup(troyka, GPIO.OUT, initial=1)

number = [0]*8

def dec2bin(val):
    return [int(bit) for bit in format(val, "b").zfill(8)]

def adc():
    left = 0
    r = 255
    while(r - left) > 1:
        m = (r + left) // 2
        GPIO.output(dac, dec2bin(int(m)))
        time.sleep(0.001)
        if (1 - GPIO.input(comp)):
            r = m
        else:
            left = m
    return left

try:
    while True:
        print(f"Voltage is: {round(adc() * 3.3 / 256, 4)}")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
