import keyboard
import mss
import cv2 as cv
import numpy as np
from time import time, sleep
import pyautogui


class sign():
    def __init__(self,image):
        self.sign = cv.imread(image)
        self.top = 0
        self.left = 0

        self.width = self.sign.shape[1]
        self.height = self.sign.shape[0]

    def match_green(self, screen):
        scr_remove = screen[:,:,:3]
        result= cv.matchTemplate(scr_remove, self.sign, cv.TM_CCOEFF_NORMED)
        _, self.max, _, self.loc = cv.minMaxLoc(result)

        threshold = 0.70
        self.top , self.left = np.where(result >= threshold)
    def location(self):
        return self.loc
    def maxpoint(self):
        return self.max
    def draw(self,screen):
        for x,y in zip(self.left,self.top):
            cv.rectangle(screen,(x,y),(x+self.width,y+self.height),(0,0,255),2)


x=1800
y=750
sct = mss.mss()

dimensions = {
        'left': 1450,
        'top': 250,
        'width': 500,
        'height': 100
    }
green = 'green.png'

go_green = sign(green)
while True:
    scr = np.array(sct.grab(dimensions))
    go_green.match_green(scr)
    go_green.draw(scr)
    print(go_green.maxpoint())

    # if go_green.location()[0] == 94:
    #     pyautogui.click(x=x, y=y)
    #     sleep(2)
    #     pyautogui.click(x=x, y=y)
    #     sleep(2)

    if go_green.maxpoint() > 0.67:
        pyautogui.click(x=x, y=y)
        sleep(2)
        pyautogui.click(x=x, y=y)
        sleep(2)
    # sleep(.01)
    cv.imshow('screen',scr)
    cv.waitKey(1)

    if keyboard.is_pressed('q'):
        break
