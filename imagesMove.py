import os, time, random,math
from re import I
from shutil import move
import pygame as p
#initialize pygame
p.init()
win = p.display.set_mode((500,500))
p.display.set_caption("first game")
walkRight = [p.image.load("IMAGES\Game\R1.png"),p.image.load("IMAGES\Game\R2.png"),p.image.load("IMAGES\Game\R3.png"),
p.image.load("IMAGES\Game\R4.png"),p.image.load("IMAGES\Game\R5.png"),p.image.load("IMAGES\Game\R6.png"),
p.image.load("IMAGES\Game\R7.png"),p.image.load("IMAGES\Game\R8.png"),p.image.load("IMAGES\Game\R9.png")]
x = 50
y = 425
width = 64
height = 64
move = 5
isJump = False
jumpCount = 10
left = False
right = False
walkCount = 0

def redrawgamewindow():
    global walkCount
    win.blit(bg, (0,0))
    if walkCount + 1 > 27:
        walkCount = 0
    if left:
        win.blit(walkLeft[walkCount//3], (x,y))
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount//3], (x,y))
        walkCount += 1
    else:
        win.blit(char, (x,y))
    p.display.update()
   
clock = p.time.Clock()
#mainloop
run = True
while run:
    clock.tick(27)
   
    redrawgamewindow()
    for event in p.event.get():
        if event.type == p.QUIT:
            run = False
    keys = p.key.get_pressed()
    if keys[p.K_LEFT] and x > move:
        x -= move
        left = True
        right = False
    elif keys[p.K_RIGHT] and x < 500 - width - move:
        x += move
        right = True
        left = False
    else:
        left = False
        right = False
        walkCount = 0
    if not (isJump):
        if keys[p.K_SPACE]:
            isJump = True
            right = False
            left = False
            walkCount = 0
    else:
        if jumpCount >= -10:
            neg = 1
            if jumpCount < 0:
                neg = -1
            y -= (jumpCount ** 2) * 0.5 * neg
            jumpCount -= 1
        else:
            isJump = False
            jumpCount = 10
p.quit()
