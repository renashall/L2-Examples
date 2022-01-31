#IMPORT LIBRARIES AND MODULES
import pygame
import time
import random
from joystick import *

#INITIALIZE PYGAME
pygame.init()
 
#LIST OF COLORS
RED = [255, 0, 0]
GREEN = [0, 255, 0]
BLUE = [0, 0, 255]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
 
#VARIABLES
length = 400
height = 300
snakeBlock = 10
snakeSpeed = 15
 
display = pygame.display.set_mode((length, height))
pygame.display.set_caption("Snake Game")
 
clock = pygame.time.Clock()
fontSize = length//24 #Base the font size on the display size
fontStyle = pygame.font.SysFont("comicsansms", fontSize)
 
def message(msg, color):
    mesg = fontStyle.render(msg, True, color)
    mesgWidth = mesg.get_width()
    mesgHeight = mesg.get_height()
    display.blit(mesg, [length/2-mesgWidth/2, height/2-mesgHeight/2])
 
def Score(score):
    value = fontStyle.render("Your Score: " + str(score), True, BLUE)
    display.blit(value, [0, 0])
 
def GameEnd():
    pygame.quit()
    destroy()
    quit()
 
def GameLoop():
    global adc
    gameOver = False
    gameClose = False
 
    #Set Initial Head Position
    x = length/2
    y = height/2
 
    #Initialize list of Snake blocks
    snakeList = [[x, y], [x-snakeBlock, y], [x-2*snakeBlock, y]]
    snakeLength = 3
 
    #Randomly generate coordinates for the food
    foodx = round(random.randrange(0, length-snakeBlock)/10.0)*10.0
    foody = round(random.randrange(0, height-snakeBlock)/10.0)*10.0
    food_spawn = True
 
    #Set initial movement direction
    direction = 'RIGHT'
    change_to = direction
 
    while not gameOver:
        # Read x, y, z values here
        val_X, val_Y, val_Z = read(adc)
 
        while gameClose == True:
            display.fill(BLACK)
            message("Game Over. Press Y to play again, press N to exit.", RED)
            Score(snakeLength - 3)
            pygame.display.update()
 
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_y:
                        GameLoop()
                    if event.key == pygame.K_n:
                        gameOver = True
                        gameClose = False
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameOver = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                    
        # ADD JOYSTICK CONTROLS HERE !
        if val_X < 64 and val_X <= val_Y:
            change_to = 'LEFT'
        if val_X > 192 and val_X >= val_Y:
            change_to = 'RIGHT'
        if val_Y < 64 and val_Y < val_X:
            change_to = 'UP'
        if val_Y > 192 and val_Y > val_X:
            change_to = 'DOWN'
 
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
 
        if direction == 'UP':
            y -= snakeBlock
        if direction == 'DOWN':
            y += snakeBlock
        if direction == 'LEFT':
            x -= snakeBlock
        if direction == 'RIGHT':
            x += snakeBlock
 
        snakeList.insert(0, [x, y])   #Add head to list of snake blocks
        if x == foodx and y == foody: #Snake found food.
            snakeLength += 1
            food_spawn = False
        else:                         #Snake didn't find food yet.
            snakeList.pop()
 
        while not food_spawn:    #Add new food block
            foodx = round(random.randrange(0, length-snakeBlock)/10.0)*10.0
            foody = round(random.randrange(0, height-snakeBlock)/10.0)*10.0
            food_spawn = True
            for i in snakeList:  #Check if selected coordinates aren't already occupied
                if i[0] == foodx and i[1] == foody:
                    food_spawn = False 
 
        if x >= length or x <= 0 or y >= height or y <= 0:
            gameClose = True     #Hit a wall.
        for i in snakeList[1:]:
            if i[0] == x and i[1] == y:
                gameClose = True #Hit a body segment
 
        display.fill(BLACK)
        for pos in snakeList:
            pygame.draw.rect(display, GREEN, pygame.Rect(pos[0], pos[1], snakeBlock, snakeBlock))
        pygame.draw.rect(display, WHITE, pygame.Rect(foodx, foody, snakeBlock, snakeBlock))
        Score(snakeLength-3)
        pygame.display.update()
        clock.tick(snakeSpeed)
 
    print("Game Over")
    exit()
 
adc = setup()
GameLoop()