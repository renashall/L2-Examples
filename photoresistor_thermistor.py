import RPi.GPIO as GPIO
import time
from calc_light_temp import light, temp
from ADCDevice import *
from ADC_helper import check_ADC

def setup():
    adc = ADCDevice()
    adc = check_ADC(adc)
    return adc

def loop():
    unit = 'F'
    while True:
        print("The temperature is " + str(round(temp(adc.analogRead(0)),2)) + "F")
        print("The light level is " + str(round(light(adc.analogRead(1)),2)) + " lumens")
        time.sleep(0.1)

if __name__ == '__main__':
    print('Program is starting...')
    adc = setup()
    try:
        loop()
    except KeyboardInterrupt:
        adc.close()
        