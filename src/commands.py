#Autoscroller

import pyautogui
import time
from FaceTracker import *

class Scroll:
    def __init__(self):
        self.scrollrate = 20
    def up(self):
        pyautogui.scroll(self.scrollrate) #scroll up by n
    def down(self):
        pyautogui.scroll(-self.scrollrate) #scroll down by n (-n)
    def setscrollrate(self, rate):
        self.scrollrate = rate
    def getscrollrate(self):
        return self.scrollrate

#head_up and head_down will be passed in by Ari/Rustam's part

# https://automatetheboringstuff.com/chapter18/