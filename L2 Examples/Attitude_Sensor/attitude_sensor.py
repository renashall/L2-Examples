import MPU6050 
import time

accel = [0]*3                                                          # define an array to store accelerometer data
gyro = [0]*3                                                           # define an array to store gyroscope data

def setup():
    mpu = MPU6050.MPU6050()                                            # instantiate a MPU6050 class object
    mpu.dmp_initialize()                                               # initialize MPU6050
    return mpu

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
        loop()
    except KeyboardInterrupt:
        exit()