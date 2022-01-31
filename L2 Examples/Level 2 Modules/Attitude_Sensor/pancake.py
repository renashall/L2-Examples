import pygame
from _thread import *
from predict import *
from attitude_sensor_data_ML import *
import MPU6050 
import time, os, csv, numpy, statistics, requests

accel = [0]*3                 # define an array to store accelerometer data
gyro = [0]*3                  # define an array to store gyroscope data
SAMPLES = 25
MEASUREMENTS = 5              # number of readings to take for each sample
INTERVAL = 0.025              # time between measuerments

set_model_ID(modelID)
mpu = setup()
answer = None
prev_answer = None
flip_detected = False

def get_prediction():
    global answer, prev_answer, flip_detected, mpu
    prediction = None
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
        prev_answer = answer
        answer = classify(data)["predictions"][0]
        if answer == 1 and answer != prev_answer:
            flip_detected = True
        else:
            flip_detected = False
        time.sleep(INTERVAL)
        
start_new_thread(get_prediction, ())
pygame.init()
WIDTH = 800
HEIGHT = 600
PANSIZE = 500
CAKESIZE = 300
CAKE_CENTER = 260
ANIMATION_FRAMES = 20
times = [25, 75, 140, 170, 190, 200, 240, 350]
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Flip!")
my_font = pygame.font.SysFont("Arial", 48)
keep_going = True
loc = [int(WIDTH/2), int(HEIGHT/2)]
flip = False

panimg = pygame.image.load('pan.png')
p0 = pygame.image.load('pcake-2.png')
p1 = pygame.image.load('pcake-1.png')
p2 = pygame.image.load('pcake0.png')
p3 = pygame.image.load('pcake1.png')
p4 = pygame.image.load('pcake2.png')
p5 = pygame.image.load('pcake3.png')
p6 = pygame.image.load('pcake4.png')
p7 = pygame.image.load('pcake5.png')

cakes = [p0, p1, p2, p3, p4, p5, p6, p7]
points = [0, 5, 15, 50, 100, 40, 20, 0]

cakeimg = p0
pcake = pygame.transform.scale(cakeimg, (CAKESIZE, CAKESIZE))
cakeRect = pcake.get_rect(center=(CAKE_CENTER, int(HEIGHT/2)))

pan = pygame.transform.scale(panimg, (750, 450))
panRect = pan.get_rect(center=(int(WIDTH/2), int(HEIGHT/2)))

cake_height = CAKESIZE
framecount = 0
flipcount = 0
prev_state = 0
while keep_going:
    framecount += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keep_going = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not flip:
                flip = True
                a_count = ANIMATION_FRAMES
    
    if flip_detected:
        if not flip:
            flip = True
            a_count = ANIMATION_FRAMES
            
    if framecount < 0:
        flip = False
    
    if framecount > times[7]:
        cakeimg = cakes[7]
    elif framecount > times[6]:
        cakeimg = cakes[6]
    elif framecount > times[5]:
        cakeimg = cakes[5]
    elif framecount > times[4]:
        cakeimg = cakes[4]
    elif framecount > times[3]:
        cakeimg = cakes[3]
    elif framecount > times[2]:
        cakeimg = cakes[2]
    elif framecount > times[1]:
        cakeimg = cakes[1]
    elif framecount > times[0]:
        cakeimg = cakes[0]

    screen.fill((0, 0, 0))    
    if flip:
        framecount = 0
        if a_count > int(ANIMATION_FRAMES/2):
            cake_height -= int(max(((cake_height/ANIMATION_FRAMES) * 6), 1))
        elif a_count == int(ANIMATION_FRAMES/2):
            if (flipcount % 2) == 0:
                prev_state = cakeimg
                cakeimg = cakes[0]
            else:
                score = int((points[cakes.index(prev_state)] + points[cakes.index(cakeimg)]) / 2)
                cakeimg = prev_state
        elif 1 < a_count < int(ANIMATION_FRAMES/2):
            cake_height += int(max(((cake_height/ANIMATION_FRAMES) * 6), 1))
        elif a_count == 1:
            cake_height = CAKESIZE
        a_count -= 1
        if a_count == 0:
            flipcount += 1
            if (flipcount % 2) == 0:
                framecount = -100
            flip = False
            
    pcake = pygame.transform.scale(cakeimg, (cake_height, CAKESIZE))
    cakeRect = pcake.get_rect(center=(CAKE_CENTER, int(HEIGHT/2)))
    
    screen.blit(pan, panRect)          
    if framecount < -20:
        screen.blit(pcake, cakeRect)
        text = my_font.render(str(score), True, (50, 255, 80))
        text_rect = text.get_rect(center=(CAKE_CENTER, int(HEIGHT/2)))
        screen.blit(text, text_rect)
    elif -20 < framecount < 0:
        cakeimg = cakes[0]
    elif framecount >= 0:   
        screen.blit(pcake, cakeRect)
        
    pygame.display.update()
pygame.quit()
            