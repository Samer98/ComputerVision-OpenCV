import keyboard
import mss
import cv2 as cv
import numpy as np
from time import time, sleep
import pyautogui


#define class for pipe
class Pipe():
    def __init__(self):
        self.image=cv.imread("upper2.png")
        self.top = [0]
        self.left = [0]
        self.width = self.image.shape[1]
        self.height = self.image.shape[0]-30
        self.space_between_pipes = 150
    def get_bottom_pipe_top(self):

        if len(self.left) == 0:
            return 0
        else:
            return self.left[0] + self.height + self.space_between_pipes

    def match(self,screen):
        scr_remove = screen[:,:,:3]
        result = cv.matchTemplate(scr_remove,self.image,cv.TM_CCOEFF_NORMED)
        threshold = 0.487
        self.left , self.top = np.where(result >= threshold)


    def draw(self,screen):
        border=[]
        for (x,y) in zip(self.top,self.left):
            border.append([int(x),int(y),int(self.width),int(self.height)])
        border,weights = cv.groupRectangles(border,1,0.2)
        for (x,y,w,h) in border:
            cv.rectangle(screen, (x,y),(x+w , y+h ), (0,255,0),2)
            cv.line(screen,(x, y+h+self.space_between_pipes),(x+w,y+h+self.space_between_pipes),(0,255,0),2)
        if len(self.left) == 0:
            return 0
        else:
            cv.circle(screen, (self.top[0],self.get_bottom_pipe_top()),3, (0,0,255),2)

    def right(self):
        return self.top[0] + self.width

    def bottom(self):
        return self.left[0] + self.height

#define the class for bird
class Player():
    def __init__(self):
        self.image=cv.imread("bird.png")
        self.top = 160
        self.left = 300
        self.width = self.image.shape[1]
        self.height = self.image.shape[0]

    def match(self,screen):
        scr_remove = screen[:,:,:3]
        result = cv.matchTemplate(scr_remove,self.image,cv.TM_CCOEFF_NORMED)
        threshold = 0.35
        self.left , self.top = np.where(result >= threshold)

    def draw(self,screen):
        border=[]
        for (x,y) in zip(self.top,self.left):
            border.append([int(x),int(y),int(self.width),int(self.height)])
        border,weights = cv.groupRectangles(border,1,0.2)
        for (x,y,w,h) in border:
             cv.rectangle(screen, (x,y),( x + w , y + h), (0,0,255),2)
        if len(self.left) == 0:
            return 0
        else:
            cv.circle(screen, (self.top[0],self.left[0]+self.height),3, (0,0,255),2)
    def get_bottom(self):
        if len(self.left) == 0:
            return 0
        else:
            return self.left[0]+self.height;

    def print(self):
        print(self.left)
    def jump(self):
        pyautogui.click(1420,90)
    def reset(self):
        self.top = 160
        self.left = 300
        self.width = self.image.shape[1]
        self.height = self.image.shape[0]

#====================================================================================


sct = mss.mss()
dimensions = {
        'left': 1400,
        'top': 80,
        'width': 500,
        'height': 600
    }



#import pictures
flappy_map = cv.imread("flappy pic.jpg")
upper_pipe = cv.imread("upper2.png")
bird=cv.imread("bird.png")
#lower_pipe = cv.imread("lower pipe.png")
pipe = Pipe()
player = Player()
player.print()
fps_time = time()
while True:

    scr = np.array(sct.grab(dimensions))

    if keyboard.is_pressed('h'):
        player.jump()
    pipe.match(scr)
    pipe.draw(scr)
    player.match(scr)
    player.draw(scr)
    # if(player.get_bottom() < pipe.get_bottom_pipe_top()):
    #     player.jump()


    print('FPS: {}'.format(1 / (time() - fps_time)))
    fps_time = time()
    cv.imshow("map",scr)
    cv.waitKey(1)
    if keyboard.is_pressed('r'):
        pyautogui.click(1542,460)
       # player.reset()
    if keyboard.is_pressed('q'):
        break
