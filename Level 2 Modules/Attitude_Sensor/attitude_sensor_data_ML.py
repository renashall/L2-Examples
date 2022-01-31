import MPU6050 
import time, os, csv, numpy, statistics, requests
from predict import *
from attitude_sensor import *

accel = [0]*3                                          # define an array to store accelerometer data
gyro = [0]*3                                           # define an array to store gyroscope data
SAMPLES = 25
MEASUREMENTS = 5                                       # number of readings to take for each sample
INTERVAL = 0.15                                        # time between measuerments

modelID = "YOUR MODEL ID HERE"

def testModel():
    prediction = None
    mpu = setup()
    set_model_ID(modelID)
    data = []
    x = []
    y = []
    z = []
    a_x = []
    a_y = []
    a_z = []
    for t in range(MEASUREMENTS):
        accel = mpu.get_acceleration()
        gyro = mpu.get_rotation()
        x.append(accel[0]/16384.0)
        y.append(accel[1]/16384.0)
        z.append(accel[2]/16384.0)
        a_x.append(gyro[0]/131.0)
        a_y.append(gyro[1]/131.0)
        a_z.append(gyro[2]/131.0)
        time.sleep(INTERVAL)
    while True:
        x.pop(0)
        y.pop(0)
        z.pop(0)
        a_x.pop(0)
        a_y.pop(0)
        a_z.pop(0)
        accel = mpu.get_acceleration()
        gyro = mpu.get_rotation()
        x.append(accel[0]/16384.0)
        y.append(accel[1]/16384.0)
        z.append(accel[2]/16384.0)
        a_x.append(gyro[0]/131.0)
        a_y.append(gyro[1]/131.0)
        a_z.append(gyro[2]/131.0)
        y_cord = numpy.array(list(range(MEASUREMENTS)))
        data = []
        for d in [x, y, z, a_x, a_y, a_z]:
            r = (max(d) - min(d))
            std = statistics.stdev(d)
            d = numpy.array(d)
            m, b = numpy.polyfit(d, y_cord, 1)
            a, b, c = numpy.polyfit(d, y_cord, 2)
            data += [r, std, m, a]
        answer = classify(data)["predictions"][0]
        if answer == 0:
            prediction = "still"
        elif answer == 1:
            prediction = "flip"
        print("Prediction: ", prediction)
        time.sleep(INTERVAL)
        
def collectData():
    headers = []
    for i in [ "x", "y", "z", "ang_x", "ang_y", "ang_z"]:
        for j in [ "_range", "_std", "_m", "_a"]:
            headers.append(j + i)
    headers.append("label")
    if not os.path.exists("attitude_data.csv"):
        with open("attitude_data.csv", "w") as log:
            headerwriter = csv.writer(log, delimiter=',')
            headerwriter.writerow(headers)
    if not os.path.exists("attitude_labels.csv"):
        with open("attitude_labels.csv", "w") as labels:
            labels.write("label, environment\n")
        label_count = -1
    else:
        with open("attitude_labels.csv", "r") as labels:
            l = labels.read()
        l = l.split('\n')
        l = l[len(l) - 2].split(',')
        l = l[len(l) - 3]
        label_count = int(l)
    collecting = True
    new_environment = True
    with open("attitude_data.csv", "a") as log, open("attitude_labels.csv", "a") as labels:
        datawriter = csv.writer(log, delimiter=',')
        while collecting:
            if new_environment:
                label_count += 1
                environment = input("Gesture name: ")
                labels.write("{},{},\n".format(label_count, environment))
            print("Data label is" , label_count, "for gesture", environment)
            for i in range(SAMPLES):
                data = []
                x = []
                y = []
                z = []
                a_x = []
                a_y = []
                a_z = []
                input("Press enter to begin recording sample " + str(i + 1) + " of " + str(SAMPLES) + " samples")
                print("3")
                time.sleep(0.2)
                print("2")
                time.sleep(0.2)
                print("1")
                time.sleep(0.2)
                print("BEGIN")
                for t in range(MEASUREMENTS):
                    accel = mpu.get_acceleration()
                    gyro = mpu.get_rotation()
                    x.append(accel[0]/16384.0)
                    y.append(accel[1]/16384.0)
                    z.append(accel[2]/16384.0)
                    a_x.append(gyro[0]/131.0)
                    a_y.append(gyro[1]/131.0)
                    a_z.append(gyro[2]/131.0)
                    time.sleep(INTERVAL)
                y_cord = numpy.array(list(range(MEASUREMENTS)))
                for d in [x, y, z, a_x, a_y, a_z]:
                    r = (max(d) - min(d))
                    std = statistics.stdev(d)
                    d = numpy.array(d)
                    m, b = numpy.polyfit(d, y_cord, 1)
                    a, b, c = numpy.polyfit(d, y_cord, 2)
                    data += [r, std, m, a]
                data.append(label_count)
                datawriter.writerow(data)
                print("END")
                print(data)
                time.sleep(0.5)
            decision = input("Continue collecting? (y/n) ").lower()
            if decision == "y":
                new_environment = (input("New gesture? (y/n) ").lower() == "y")
            else:
                collecting = False
                            
def loop():
    while True:
        accel = mpu.get_acceleration()                                 # get accelerometer data
        gyro = mpu.get_rotation()                                      # get gyroscope data
        print("Lateral Acceleration\tX: %.2f \tY: %.2f \tZ: %.2f"
            %(accel[0]/16384.0,accel[1]/16384.0,accel[2]/16384.0))
        print("Angular Acceleration\tX: %.2f \tY: %.2f \tZ: %.2f"
            %(gyro[0]/131.0,gyro[1]/131.0,gyro[2]/131.0)) 
        time.sleep(0.5)
        
if __name__ == '__main__':                                             # Program entrance
    print("Program is starting ... ")
    mpu = setup()
    try:
        choice = input("Collect data (1) or test model(2)? ")
        if choice == "collect data" or choice == "1":
            collectData()
        else:
            testModel()
    except KeyboardInterrupt:                                          # Press ctrl-c to end the program.
        exit()