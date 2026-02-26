from keyboard import add_hotkey,wait
import pyautogui
import threading
#from PIL import Image

#class that handles keyboard hotkeys
class keyboard_helper:
    def __init__(self):
        self.detecting=0
    
    # enable aimbot
    def start_detect(self):
        if self.detecting:
            # prevent multiple threads
            return  

        self.detecting = True
        threading.Thread(target=self.detect_loop, daemon=True).start()

    def detect_loop(self):
        while self.detecting:
            pyautogui.sleep(1.5)
            print("detecting")
            pass
            #img=pyautogui.screenshot()

        #quit detect
        print("detection aborted")
            
    #disable aimbot
    def quit_detect(self):
        self.detecting=0

        
        
    

detector=keyboard_helper()
add_hotkey("s",detector.start_detect)
add_hotkey("p",detector.quit_detect)
#wait('esc')

pyautogui.moveTo(1915, 1075)
