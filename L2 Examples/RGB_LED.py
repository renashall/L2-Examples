import RPi.GPIO as GPIO
import time
from ADCDevice import *
from ADC_helper import check_ADC

ledRedPin = 15
ledGreenPin = 13
ledBluePin = 11
adc = ADCDevice()

def setup():
    global adc
    adc = check_ADC(adc)
    global p_Red, p_Green, p_Blue
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledRedPin, GPIO.OUT)
    GPIO.setup(ledGreenPin, GPIO.OUT)
    GPIO.setup(ledBluePin, GPIO.OUT)

    p_Red = GPIO.PWM(ledRedPin, 1000)
    p_Red.start(0)
    p_Green = GPIO.PWM(ledGreenPin, 1000)
    p_Green.start(0)
    p_Blue = GPIO.PWM(ledBluePin, 1000)
    p_Blue.start(0)

def loop():
    while True:
        val_Red = adc.analogRead(0)
        val_Green = adc.analogRead(1)
        val_Blue = adc.analogRead(2)
        p_Red.ChangeDutyCycle(val_Red*100/255)
        p_Green.ChangeDutyCycle(val_Green*100/255)
        p_Blue.ChangeDutyCycle(val_Blue*100/255)
        i_red = 100*(255 - val_Red)/255
        i_green = 100*(255 - val_Green)/255
        i_blue = 100*(255 - val_Blue)/255
        print("Red value: %d \t\t Green value: %d \t\t Blue value: %d" %
            (val_Red, val_Green, val_Blue))
        print("Red intensity: %.2f \t Green intensity: %.2f \t Blue intensity: %.2f" %
            (i_red, i_green, i_blue))
        time.sleep(0.1)

def destroy():
    adc.close()
    GPIO.cleanup()

if __name__ == '__main__':
    print("Program is starting...")
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()
