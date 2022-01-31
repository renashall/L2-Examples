import RPi.GPIO as GPIO
import time
from ADCDevice import *
from ADC_helper import *

Z_Pin = 12

def setup():
    adc = ADCDevice()
    adc = check_ADC(adc)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(Z_Pin,GPIO.IN, GPIO.PUD_UP)
    return adc

def read(adc):
    val_Z = GPIO.input(Z_Pin)
    val_Y = adc.analogRead(0)
    val_X = adc.analogRead(1)
    return val_X, val_Y, val_Z
    
def loop():
    while True:
        print("Value X: %d \t Value Y: %d \t Value Z: %d" %
            (read(adc)))
        time.sleep(0.1)

def destroy():
    adc.close()
    GPIO.cleanup()

if __name__ == '__main__':
    print('Program is starting...')
    adc = setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()