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
import time
import ctypes
from mouse_handler import mouse_handler




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
        self.timing=True
        self.mouse=mouse_handler()
    
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
        self.mouse.start_tracking()
        pyautogui.sleep(1.5)
        dx=600
        dy=0

        x,y=win32api.GetCursorPos()        
        img=pyautogui.screenshot()
        plt.imshow(img)
        plt.plot(x,y,marker='o',color='green')
        plt.plot(x+dx,y+dy,marker='x',color='r')
        plt.axis('off')
        plt.savefig("before.png")
        plt.clf()
        yoff=self.mouse.get_y()
        self.mouse.move_mouse(0,-yoff)
        self.mouse.move_mouse(int(dx/coeff(dx)), 0)
        self.mouse.move_mouse(0,yoff)
        self.mouse.move_mouse(0, int(dy/coeff(dy)))

        left_click()
        pyautogui.sleep(0.2)

        img=pyautogui.screenshot()
        plt.imshow(img)
        plt.axis('off')
        plt.plot(x,y,marker='o',color='green')
        plt.savefig("after.png")
        self.detecting=0


    #check if model detected an enemy
    def enemy_check(self,prediction):
        return np.sum(prediction)/np.size(prediction>0.02)
            
            

            
    #disable aimbot
    def quit_detect(self):
        print('trying to quit detection...')
        self.detecting=0
    #reset mouse tracking
    def reset_tracking(self):
        self.mouse.reset_tracking()

#dx=600->1.47   
#300->1.25
#100->1.2
#900->1.65
sensitivity=1.25
coeff=lambda x:1.05+x*0.00067
trasposey=1.25
print('--- Initializing aimbot')
detector=keyboard_helper()
add_hotkey("shift+p",detector.start_detect)
add_hotkey("shift+l",detector.quit_detect)
add_hotkey("shift+o",detector.reset_tracking)

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