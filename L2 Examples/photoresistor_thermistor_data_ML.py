import RPi.GPIO as GPIO
import time, math, os, requests
from ADCDevice import *
from photoresistor_thermistor import *
from predict import *

SAMPLES = 50

modelID = "2a4fcc8c-fe24-4c66-8167-99a9f4f28862"

def testModel():
    prediction = None
    global adc
    set_model_ID(modelID)
    while True:
        l = round(light(adc.analogRead(1)),4)
        t = round(temp(adc.analogRead(0)),2)
        data = [l, t]
        print("Light:", data[0], "Temperature:", data[1])
        answer = classify(data)["predictions"][0]
        if answer == 0:
            prediction = "no sun"
        elif answer == 1:
            prediction = "sun has risen"
        print("Prediction: ", prediction)
        time.sleep(2)
        
def logData(data, log, label):
    if len(data) == 2:
        log.write("{},{},{},\n".format(data[0],data[1],label))

def collectData():
    global adc
    if not os.path.exists("photoresistor_data.csv"):
        with open("photoresistor_data.csv", "w") as log:
            log.write("light,temp,label\n")
    if not os.path.exists("photoresistor_labels.csv"):
        with open("photoresistor_labels.csv", "w") as labels:
            labels.write("label, environment\n")
        label_count = -1
    else:
        with open("photoresistor_labels.csv", "r") as labels:
            l = labels.read()
        l = l.split('\n')
        l = l[len(l) - 2].split(',')
        l = l[len(l) - 3]
        label_count = int(l)
    collecting = True
    new_environment = True
    with open("photoresistor_data.csv", "a") as log, open("photoresistor_labels.csv", "a") as labels:
        while collecting:
            if new_environment:
                label_count += 1
                environment = input("Data environment name: ")
                labels.write("{},{},\n".format(label_count, environment))
            print("Data label is" , label_count, "for environment", environment)
            input("press enter to log " + str(SAMPLES) + " samples")
            sumCnt = 0
            for i in range(SAMPLES):
                print("\nReading", sumCnt)
                l = round(light(adc.analogRead(1)),4)
                t = round(temp(adc.analogRead(0)),2)
                sumCnt += 1  
                logData([l, t], log, label_count)
                print([l, t])
                time.sleep(0.5)
            decision = input("Continue collecting? (y/n) ").lower()
            if decision == "y":
                new_environment = (input("New environment? (y/n) ").lower() == "y")
            else:
                collecting = False

if __name__ == '__main__':
    print('Program is starting...')
    adc = setup()
    try:
        choice = input("Collect data (1) or test model(2)? ")
        if choice == "collect data" or choice == "1":
            collectData()
        else:
            testModel()
    except KeyboardInterrupt:
        adc.close()