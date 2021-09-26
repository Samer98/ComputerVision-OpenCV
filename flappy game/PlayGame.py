import keyboard
import mss
import cv2 as cv
import numpy as np
from time import time, sleep
import pyautogui

# top = x_axis
# left= y_axis
#define class for pipe
class Pipe():
    def __init__(self):
        self.image=cv.imread("upper2.png")
        self.top = 0
        self.left = 0
        self.width = self.image.shape[1]
        self.height = self.image.shape[0]-30
        self.space_between_pipes = 150

    def get_upper_pipe_bottom(self):
        if len(self.left) == 0:
            return 0
        else:
            return self.left[0] + self.height

    def get_bottom_pipe_top(self):

        if len(self.left) == 0:
            return 1000
        else:
            return self.left[0] + self.height + self.space_between_pipes

    def get_left(self):
        if len(self.top) == 0:
            return 1000
        else:
            return self.top[0]

    def get_right(self):
        if len(self.top) == 0:
            return 0
        else:
            return self.top[0]+self.width

    def get_middle_y(self):
        if len(self.left) == 0:
            return 800
        return  self.get_upper_pipe_bottom() + self.space_between_pipes

    def get_middle_x(self):
        if len(self.top) == 0:
            return 0
        else:
            return (self.top[0] + self.width)

    def match(self,screen):
        scr_remove = screen[:,:,:3]
        result = cv.matchTemplate(scr_remove,self.image,cv.TM_CCOEFF_NORMED)
        threshold = 0.487
        self.left, self.top = np.where(result >= threshold)

    def draw(self,screen):
        border=[]
        for (x,y) in zip(self.top,self.left):
            border.append([int(x),int(y),int(self.width),int(self.height)])
        border,weights = cv.groupRectangles(border,1,0.2)
        for (x,y,w,h) in border:
            cv.rectangle(screen, (x,y) ,(x + w, y + h), (0,255,0),2)
            cv.line(screen,(x, y+h+self.space_between_pipes),(x+w,y+h+self.space_between_pipes),(0,255,0),2)
        p1 = (self.get_left(),self.get_upper_pipe_bottom()-self.height)
        p2 = (self.get_right(), self.get_upper_pipe_bottom())
        cv.rectangle(screen, p1,p2, (255,50,255),2)
        cv.circle(screen,(self.get_left(),self.get_upper_pipe_bottom()),3,(0,255,0),2)
        cv.circle(screen,(self.get_right(),self.get_upper_pipe_bottom()),3,(0,255,0),2)
        cv.circle(screen,(self.get_left(),self.get_bottom_pipe_top()),3,(0,255,0),2)
        cv.circle(screen,(self.get_right(),self.get_bottom_pipe_top()),3,(0,255,0),2)

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


        cv.circle(screen,(self.get_left(),self.get_bottom()),3,(0,255,0),2)
        cv.circle(screen,(self.get_right(),self.get_bottom()),3,(0,255,0),2)
        cv.circle(screen,(self.get_left(),self.get_top()),3,(0,255,0),2)
        cv.circle(screen,(self.get_right(),self.get_top()),3,(0,255,0),2)


        cv.circle(screen,(int(self.get_middle_x()),int(self.get_middle_y())), 3, (255,255,0),2)

    def get_top(self):
        if len(self.left) == 0:
            return 1000
        else:
            return self.left[0]

    def get_left(self):
        if len(self.top) == 0:
            return 1000
        else:
            return self.top[0]

    def get_bottom(self):
        if len(self.left) == 0:
            return 0
        else:
            return self.left[0]+self.height

    def get_right(self):
        if len(self.left) == 0:
            return 0
        else:
            return self.top[0]+self.width

    def get_middle_y(self):
        if len(self.left) == 0:
            return 0
        else:
            return self.left[0] + (self.height/2)

    def get_middle_x(self):
        if len(self.top) == 0:
            return 0
        else:
            return self.top[0] + (self.width/2)

    def jump(self):
        pyautogui.click(1420,90)
    def reset(self):
        self.top = 160
        self.left = 300
        self.width = self.image.shape[1]
        self.height = self.image.shape[0]


#====================================================================================

def detect_collison(player , pipe):
    if(
            player.get_top() < pipe.get_upper_pipe_bottom() &
            player.get_right() > pipe.get_left()
    ):
        print("i got killed by hitting left corner of upper pipe")
    elif(player.get_top() < pipe.get_upper_pipe_bottom() &
            player.get_left() > pipe.get_right()
    ):
        print("i got killed by hitting right corner of upper pipe")
    elif(player.get_bottom() > pipe.get_bottom_pipe_top() &
            player.get_right() > pipe.get_left()
    ):
        print("i got killed by hitting left corner of bottom pipe")
    elif(player.get_bottom() > pipe.get_bottom_pipe_top() &
            player.get_left() < pipe.get_right()
    ):
        print("i got killed by hitting right corner of bottom pipe")
sct = mss.mss()
# dimensions = {
#         'left': 1400,
#         'top': 80,
#         'width': 500,
#         'height': 600
#     }

dimensions = {
        'left': 0,
        'top': 0,
        'width': int(1980/2.5),
        'height': 1080
    }

#import pictures
flappy_map = cv.imread("flappy pic.jpg")
upper_pipe = cv.imread("upper2.png")
bird=cv.imread("bird.png")
#lower_pipe = cv.imread("lower pipe.png")
pipe = Pipe()
player = Player()
fps_time = time()
last_jump_time = 0
center_jump_time = 0
while True:

    scr = np.array(sct.grab(dimensions))

    if keyboard.is_pressed('h'):
        player.jump()
    pipe.match(scr)
    pipe.draw(scr)
    player.match(scr)
    player.draw(scr)
    detect_collison(player,pipe)
    # #if (player.get_top() < pipe.get_upper_pipe_bottom() & player.get_top() > )
    # if (player.get_top() < pipe.get_upper_pipe_bottom()):
    #     print("not jumping because iam over the top pipe")
    # # elif (player.get_middle_y() > pipe.get_middle_y()):
    # #     print("jumping to become in center of 2 pipes")
    # #     player.jump()
    # elif (player.get_bottom() > pipe.get_bottom_pipe_top()):
    #     if (time()-last_jump_time > 0.500):
    #         last_jump_time = time()
    #         print("jumping to save my stomach from hitting the bottom pipe")
    #         player.jump()
    #     else:
    #         print('i must jump again to save my stomach but daddy told me to wait for some time')
    #
    # # elif(player.get_bottom() > pipe.get_bottom_pipe_top()-50):
    # #     player.jump()
    # #     sleep(0.3)
    # elif player.get_middle_y() > 375:
    #     if (time()-center_jump_time > 0.500):
    #         center_jump_time = time()
    #         print("jumping to be in center of screen")
    #         player.jump()
    #     else:
    #         print('i wont jump cause i am already jumped')

    #print('FPS: {}'.format(1 / (time() - fps_time)))
    fps_time = time()
    cv.imshow("map",scr)
    cv.waitKey(1)
    if keyboard.is_pressed('r'):
        pyautogui.click(1542,460)
       # player.reset()
    if keyboard.is_pressed('q'):
        break
