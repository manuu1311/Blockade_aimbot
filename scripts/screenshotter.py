from keyboard import add_hotkey,wait
import pyautogui
#import threading
#from PIL import Image
import win32api
import win32con
#import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # <-- add BEFORE importing pyplot

import matplotlib.pyplot as plt




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


#class that handles keyboard hotkeys
class keyboard_helper:
    def __init__(self):
        self.detecting=0
        self.w, self.h = pyautogui.size()
    
    # enable aimbot
    def start_detect(self):
        if self.detecting:
            # prevent multiple threads
            return  

        self.detecting = True
        #threading.Thread(target=self.detect_loop, daemon=True).start()
        self.detect_loop()

    def detect_loop(self):
        while self.detecting:
            pyautogui.sleep(1.5)
            print("detecting")
            x,y=win32api.GetCursorPos()
            dx=575
            dy=0
            img=pyautogui.screenshot()
            print('first screen')
            plt.imshow(img)
            plt.plot(x,y,marker='o',color='green')
            plt.plot(x+dx,y+dy,marker='x',color='r')
            plt.axis('off')
            plt.savefig("before.png")
            plt.clf()
            move_mouse(dx, dy)
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
            

        #quit detect
        print("detection aborted")
            
    #disable aimbot
    def quit_detect(self):
        self.detecting=0

        
sensitivity=1.25
border=575 
    
detector=keyboard_helper()
add_hotkey("shift+p",detector.start_detect)
add_hotkey("ctrl+shift+l",detector.quit_detect)
wait('ctrl+shift+f')


#dx=150,actual:187
#dx=400,actual:499
#dx=10,actual=12
#dx=1000,actual=1250