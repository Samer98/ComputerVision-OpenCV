import keyboard
import mss
import cv2 as cv
import numpy as np
from time import time, sleep
import pyautogui
from enum import Enum

class Direction(Enum):
    left = 1
    right = 2


class wood():
    def __init__(self):
        self.woodleft = cv.imread('woodleft.jpg')
        self.woodright = cv.imread('woodright.jpg')

        self.top = 0
        self.left = 0
        self.loc = 0
        self.width = self.woodleft.shape[1]
        self.height = self.woodleft.shape[0]

    def match_wood_left(self, screen):
        scr_remove = screen[:,:,:3]
        result= cv.matchTemplate(scr_remove,self.woodleft,cv.TM_CCOEFF_NORMED)
        _, _, _, loc = cv.minMaxLoc(result)

        threshold = 0.48
        top , left = np.where(result >= threshold)
        return top , left , loc
    def match_wood_right(self, screen):
        scr_remove = screen[:,:,:3]
        result= cv.matchTemplate(scr_remove,self.woodright,cv.TM_CCOEFF_NORMED)
        _, _, _, loc = cv.minMaxLoc(result)

        threshold = 0.48
        top ,left = np.where(result >= threshold)
        return top , left , loc
    def location(self):
        return self.loc

    def draw(self,screen,left,top):
        for x,y in zip(left,top):
            cv.rectangle(screen,(x,y),(x+self.width,y+self.height),(0,0,255),2)


# class woodright():
#     def __init__(self):
#         self.wood = cv.imread('woodright.jpg')
#         self.top = 0
#         self.left = 0
#         self.loc = 0
#         self.width = self.wood.shape[1]
#         self.height = self.wood.shape[0]
#
#     def match_wood(self, screen):
#         scr_remove = screen[:,:,:3]
#         result= cv.matchTemplate(scr_remove,self.wood,cv.TM_CCOEFF_NORMED)
#         _, _, _, self.loc = cv.minMaxLoc(result)
#
#         threshold = 0.5
#         self.top , self.left = np.where(result >= threshold)
#
#     def location(self):
#         return self.loc
#
#     def draw(self,screen):
#         for x,y in zip(self.left,self.top):
#             cv.rectangle(screen,(x,y),(x+self.width,y+self.height),(0,0,255),2)

class Player():
    def __init__(self):
        self.direction = Direction.left

    def go_left(self):
        pyautogui.click(1536,637)
        self.direction = Direction.left

    def go_right(self):
        pyautogui.click(1794,637)
        self.direction = Direction.right

    def chop_ya_kick(self):
        if(self.direction == Direction.left):
            self.go_left()
        else:
            self.go_right()

# woodleft = cv.imread('woodleft.jpg')
# woodright= cv.imread('woodright.jpg')

x=1536
y=450
sct = mss.mss()

dimensions = {
        'left': 1450,
        'top': 450,
        'width': 500,
        'height': 100
    }

player = Player()
wood = wood()

while True:
    scr = np.array(sct.grab(dimensions))
    top_rightwood , left_rightwood , loc_rightwood =wood.match_wood_right(scr)
    wood.draw(scr,left_rightwood,top_rightwood)
    top_leftwood , left_leftwood ,loc_leftwood =wood.match_wood_left(scr)
    wood.draw(scr,left_leftwood,top_leftwood)
    # print(loc_leftwood[1])
    # print(loc_rightwood[1])
    if  loc_leftwood[1] == 11:
        x=1794

    elif loc_rightwood[1] == 12:
        x = 1536

    pyautogui.click(x=x, y=y)
    sleep(.10)
    cv.imshow('screen',scr)
    cv.waitKey(1)

    if keyboard.is_pressed('q'):
        break
