from keyboard import add_hotkey,wait
import pyautogui
import threading
from PIL import Image
import numpy as np
import win32api
import win32con
#import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # <-- add BEFORE importing pyplot
import matplotlib.pyplot as plt
from winsound import Beep
from model import segment_detector
import time



def move_mouse(dx, dy):
    # Move mouse by dx, dy
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, dx,dy, 0, 0)

def left_click():
    """Single left click at current mouse position"""
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def left_down():
    """Hold down left mouse button"""
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)

def left_up():
    """Release left mouse button"""
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

def beep(freq,t):
    Beep(freq,t)

#display image with model prediction, segmentation
def disp_click_segment(img,mask,x,y,name='prova'):
    img=img.convert('RGB')
    img = np.array(img)[...,:3]
    predicted_mask = mask
    color_mask = np.zeros_like(img)
    color_mask[predicted_mask == 1] = [255, 0, 0]
    # Transparency factor
    alpha = 0.5  
    blended_image = img * (1 - alpha) + color_mask * alpha
    blended_image = blended_image.astype(np.uint8)

    plt.figure(figsize=(10, 10))
    plt.imshow(blended_image)
    plt.plot(y,x,'x',markersize=10)
    plt.axis('off')
    plt.savefig(name)

disp_click=disp_click_segment

#class that handles keyboard hotkeys
class keyboard_helper:
    def __init__(self):
        self.detecting=0
        self.w, self.h = pyautogui.size()
        self.model=segment_detector()
        self.timing=True
    
    # enable aimbot
    def start_detect(self):
        if self.detecting:
            # prevent multiple threads
            return  

        self.detecting = True
        print('Turning on aimbot')
        threading.Thread(target=self.detect_loop, daemon=True).start()
        #self.detect_loop()

    def detect_loop(self):
        print('Aimbot turned on')
        beep(2000,100)
        while self.detecting:
            tf=time.time()
            screen=pyautogui.screenshot().resize(self.model.size)
            img=screen.convert('L')
            predicted=self.model.predict(img,scale=255,thresh=0.9,cleanup=True)
            if self.timing:
                print(time.time()-tf)
            if self.enemy_check(predicted):
                print('enemy detected')
                beep(1000,100)
                dx,dy=self.model.get_centroid(predicted)
                disp_click(screen,predicted,dx,dy)
                '''
                plt.imshow(img)
                plt.plot(dx,dy,marker='x',color='r',markersize=25)
                plt.axis('off')
                plt.savefig("prova.png")
                plt.clf()
                '''
            pyautogui.sleep(5.0)
        print('detection quit successfully')
        beep(500,100)

    #check if model detected an enemy
    def enemy_check(self,prediction):
        return np.sum(prediction)/np.size(prediction>0.02)
            
            

            
    #disable aimbot
    def quit_detect(self):
        print('trying to quit detection...')
        self.detecting=0

        
sensitivity=1.25
border=575 
traspose=1.669565
print('--- Initializing aimbot')
detector=keyboard_helper()
add_hotkey("shift+p",detector.start_detect)
add_hotkey("shift+l",detector.quit_detect)
print('--- Aimbot is ready, waiting for hotkey')
wait('ctrl+shift+f')







#dx=150,actual:187
#dx=400,actual:499
#dx=10,actual=12
#dx=1000,actual=1250
'''
pyautogui.sleep(1.5)
            x,y=win32api.GetCursorPos()
            dx=240
            dy=0
            img=pyautogui.screenshot()
            print('first screen')
            plt.imshow(img)
            plt.plot(x,y,marker='o',color='green')
            plt.plot(x+dx,y+dy,marker='x',color='r')
            plt.axis('off')
            plt.savefig("before.png")
            plt.clf()
            move_mouse(int(dx/traspose), dy)
            print(f'x:{x},y={y}',dx,dy)
            left_click()
            #pydirectinput.leftClick()
            pyautogui.sleep(0.2)
            print('second screen')
            x,y=win32api.GetCursorPos()
            img=pyautogui.screenshot()
            print(f'newx={x},newy={y}')
            plt.imshow(img)
            plt.plot(x,y,marker='o',color='green')
            plt.axis('off')
            plt.savefig("after.png")
            self.detecting=0
'''