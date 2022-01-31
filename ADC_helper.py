from ADCDevice import *

def check_ADC(adc_device):
    if(adc_device.detectI2C(0x48)):                                                # Detect the pcf8591
        adc = PCF8591()
    elif(adc_device.detectI2C(0x4b)):                                              # Detect the ads7830
        adc = ADS7830()
    else:
        print("No correct I2C address found, \n"
        "Please use command 'i2cdetect -y 1' to check the I2C address! \n"
        "Program Exit. \n");
        exit(-1)
    return adc
