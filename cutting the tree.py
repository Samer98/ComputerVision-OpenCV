import keyboard
import mss
import cv2 as cv
import numpy as np
from time import time, sleep
import pyautogui


class wood():
    def __init__(self,image):
        self.wood = cv.imread(image)
        self.top = 0
        self.left = 0

        self.width = self.wood.shape[1]
        self.height = self.wood.shape[0]

    def match_wood(self, screen):
        scr_remove = screen[:,:,:3]
        result= cv.matchTemplate(scr_remove, self.wood, cv.TM_CCOEFF_NORMED)
        _, _, _, self.loc = cv.minMaxLoc(result)

        threshold = 0.48
        self.top , self.left = np.where(result >= threshold)
    def location(self):
        return self.loc
    def draw(self,screen):
        for x,y in zip(self.left,self.top):
            cv.rectangle(screen,(x,y),(x+self.width,y+self.height),(0,0,255),2)


x=1536
y=450
sct = mss.mss()

dimensions = {
        'left': 1450,
        'top': 450,
        'width': 500,
        'height': 100
    }
woodleft= "woodleft.jpg"
woodright= "woodright.jpg"

woodleft_obj= wood(woodleft)
woodright_obj = wood(woodright)
while True:
    scr = np.array(sct.grab(dimensions))
    woodleft_obj.match_wood(scr)
    woodleft_obj.draw(scr)


    woodright_obj.match_wood(scr)
    woodright_obj.draw(scr)

    if woodleft_obj.loc[0] == 101:
        x=1794

    elif woodright_obj.loc[0] == 277:
        x = 1536

    pyautogui.click(x=x, y=y)
    sleep(.01)
    cv.imshow('screen',scr)
    cv.waitKey(1)

    if keyboard.is_pressed('q'):
        break
