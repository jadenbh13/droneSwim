import pygame
from math import sin,cos,radians
import random
import time
import threading

def pie(scr,color,center,radius,start_angle,stop_angle):
    theta=start_angle
    while theta <= stop_angle:
        pygame.draw.line(scr,color,center,
        (center[0]+radius*cos(radians(theta)),center[1]-radius*sin(radians(theta))),2)
        theta+=0.01

def thf(ph):
    winWidth,winHeight=500,500
    bv = 0
    mt = random.randint(0, 360)
    scr=pygame.display.set_mode((winWidth,winHeight))
    pie(scr,(255,0,0),(winWidth//2,winHeight//2),250,0,ph)
    bv += 1
    pygame.display.update()
    time.sleep(0.1)
thf(100)
