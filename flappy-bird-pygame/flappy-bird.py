import os
import sys
import serial
import pygame, math
from random import randint
from time import sleep

pygame.init()

WIDTH = 1000
HEIGHT = 580

BIRD_WIDTH = 50
BIRD_HEIGHT = 36

PIPE_WIDTH = 75
PIPE_LENGTH = 450
PIPE_GAP = 10

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird!")
bird = pygame.image.load('bird.png') 
background = pygame.image.load('bg.png')
pipeBottom = pygame.image.load('pipe.png')
pipeTop = pygame.transform.rotate(pipeBottom, 180)
font = pygame.font.SysFont('Comic Sans MS', 30)

uno = serial.Serial("/dev/cu.usbmodem14301", 115200)
uno.setDTR()
uno.flush()
if (uno.in_waiting > 10):
    uno.reset_input_buffer()

def setupGame() :
    global gameRun
    gameRun = True
    global gameOver 
    gameOver = False
    global gameStart 
    gameStart = False
    global gameRunCount
    gameRunCount = 0
    global score
    score = -2
    global pipes
    pipes = []

    Bird.birdX = 250
    Bird.birdY = 250
    Bird.vel = 0

class Bird :
    birdX = 250
    birdY = 250
    distanceVal = 0
    vel = 0  

    def read() :
        strDistance = uno.readline().strip().decode('utf-8')   

        if not strDistance:
            Bird.distanceVal = 0
        else:
            Bird.distanceVal = int(strDistance)    

        if Bird.distanceVal != 0 :
            jump = pygame.event.Event(pygame.USEREVENT)
            pygame.event.post(jump)

    def jump() :   
        if 2 < Bird.distanceVal < 30:
            Bird.vel = -Bird.distanceVal 
        else:
            Bird.vel = 0 

    def update() :
        if gameStart :   
            if Bird.birdY < (HEIGHT - BIRD_HEIGHT) : 
                Bird.birdY += Bird.vel
                Bird.vel += 1
            else :
                Bird.birdY = (HEIGHT - BIRD_HEIGHT)
                die()

            if Bird.birdY < 0 :
                Bird.birdY = 0
                Bird.vel -= 0
        else :
            Bird.birdY = 250 + math.sin(gameRunCount/10) * 15

class Pipe() :
    def __init__(self, direction, x, length) :
        self.direction = direction
        self.pipeX = x
        self.pipeLength = length

    def update(self) :
        if self.direction == "BOTTOM" :
            screen.blit(pipeBottom, (self.pipeX , HEIGHT - self.pipeLength)) 
        else :
            screen.blit(pipeTop, (self.pipeX , self.pipeLength - PIPE_LENGTH)) 
        if not gameOver :
            self.pipeX -= PIPE_GAP

    def checkCollide(self) :
        if self.direction == "TOP" :
            if Bird.birdX + BIRD_WIDTH >= self.pipeX and self.pipeX + PIPE_WIDTH >= Bird.birdX : 
                if Bird.birdY <= self.pipeLength : 
                    die()
        else :
            if Bird.birdX + BIRD_WIDTH >= self.pipeX and self.pipeX + PIPE_WIDTH >= Bird.birdX : 
                if Bird.birdY + BIRD_HEIGHT >= HEIGHT - self.pipeLength : 
                    die()

def generatePipes() :
    random = randint(100, 200)
    pipes.append(Pipe("TOP", 900, random))
    pipes.append(Pipe("BOTTOM", 900, HEIGHT - (random + BIRD_HEIGHT * 4)))
    global score
    score += 1

def die() :
    global gameOver
    gameOver = True
    gameRun = False

setupGame()

while gameRun:
    pygame.time.delay(5)

    for event in pygame.event.get() :
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_ESCAPE :
                gameRun = False
            elif event.key == pygame.K_SPACE :
                if not gameStart :
                    gameStart = True
                if not gameOver :
                    Bird.read()
                    Bird.jump()    
        elif event.type == pygame.QUIT :
            gameRun = False
        elif event.type == pygame.USEREVENT :
            if not gameOver :
                Bird.jump()

    screen.blit(background, (0,0))

    if gameRunCount % 45 == 0 and gameStart :
        generatePipes()
    for p in pipes :
        p.update()
        p.checkCollide()

    Bird.update()
    screen.blit(bird, (Bird.birdX, Bird.birdY))

    distance = font.render(str(Bird.distanceVal), False, (0, 0, 0))
    screen.blit(distance, (20, 45))

    scoreboard = font.render(str(score), False, (255, 255, 255))
    if score > -1 :
        screen.blit(scoreboard, (20, 20))
    pygame.display.update()

    if not gameOver:
        gameRunCount += 1

pygame.quit()

