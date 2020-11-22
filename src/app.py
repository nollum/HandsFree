import tkinter as tk
from tkinter import font
import FaceTracker as ft
from PIL import Image, ImageTk
import webbrowser
import cv2
import pyautogui
import time
import constants
import os

#WINDOW
WIDTH = 600
HEIGHT = 700

face = ft.FaceTracker()

def up():
    pyautogui.scroll(50) #scroll up by n
    time.sleep(0.000001)
def down():
    pyautogui.scroll(-50) #scroll down by n (-n)
    time.sleep(0.000001)

#Moving the mouse relative to its current position
def move_mouse(n, m):
    if check_mouse_loc():
        if n != 0 and m != 0:
            pyautogui.moveRel((n/abs(n))*constants.scrollrate, -(m/abs(m))*constants.scrollrate, 0.1) #scroll down by n (-n)
        elif n != 0:
            pyautogui.moveRel((n/abs(n))*constants.scrollrate, 0, 0.1) #scroll down by n (-n)
        else:
            pyautogui.moveRel(0, -(m/abs(m))*constants.scrollrate, 0.1) #scroll down by n (-n)
    else:
        width, height = pyautogui.size()
        pyautogui.moveTo(width/2, height/2, duration=0.25)

def check_mouse_loc():
    mouse_x, mouse_y = pyautogui.position()
    width, height = pyautogui.size()
    if mouse_x <= 20 and (mouse_y <= 20 or mouse_y >= height-20):
        return False
    elif mouse_x >= width - 20 and (mouse_y <= 20 or mouse_y >= height-20):
        return False
    else:
        return True

#Click the mouse at current position
def click():
    pyautogui.click() #by default, this left-clicks at the current (x, y) cursor position

root = tk.Tk()
root.option_add('*Font', '19')
root.title("Auto-Scroller")
root.geometry("{}x{}".format(WIDTH, HEIGHT))
root.geometry('+{}+{}'.format(100,100))
root.resizable(False, False)
root.option_add("*Font", ("Consolas", 20))

def showDirection(dir):
    if dir == 1:
        return 'Down'
    elif dir == 2:
        return 'Up'
    elif dir == 3:
        return 'No movement'
    else:
        return 'Not looking at camera'

def key_pressed(event):
    endProcess()

def endProcess():
    root.geometry("{}x{}".format(WIDTH, HEIGHT))
    root.attributes('-topmost', False)
    faceDirectionLabel.config(anchor="center")
    faceDirectionLabel.pack(pady=10)
    panelButton.config(text="Start")
    panelButton.config(command=startProcess)
    panelButton.pack(fill="x")
    tutorialButton.pack(fill="x")
    panelFrame.pack(side="bottom", fill="x")
    imageFrame.config(width=orig_width, height=orig_height)

def startProcess():
    faceDirectionLabel.forget()
    tutorialButton.forget()
    panelButton.config(text="Stop")
    panelButton.config(command=endProcess)
    root.geometry("{}x{}".format(WIDTH//2, HEIGHT//2))
    imageFrame.config(width=WIDTH//2, height=HEIGHT//2-panelButton.winfo_height())
    root.attributes('-topmost', True)
    root.bind("<Key>", key_pressed)
    while imageFrame['width'] == WIDTH//2:
        nose_x, nose_y = face.get_nose_direction()
        if face.get_direction() == 1:
            down()
        elif face.get_direction() == 2: 
            up()
        elif abs(nose_x) > constants.horizontal_x_sens and abs(nose_y) > constants.vertical_y_sens: #diagonal
            move_mouse(nose_x, nose_y)
        elif abs(nose_x) > constants.horizontal_x_sens: #horizontal
            move_mouse(nose_x, 0)
        elif abs(nose_y) > constants.vertical_y_sens: #vertical
            move_mouse(0, nose_y)
        elif face.on_click():
            click()
        elif face.on_reset():
            width, height = pyautogui.size()
            pyautogui.moveTo(width/2, height/2, duration=0.25)
        root.update()

def openTutorial():
    filename = "./site/index.html"
    webbrowser.open('file://' + os.path.realpath(filename), new=2)

def p_on_enter(bttn):
    panelButton['background'] = 'grey'

def p_on_leave(bbtn):
    panelButton['background'] = '#CACACA'

def t_on_enter(bttn):
    tutorialButton['background'] = 'grey'

def t_on_leave(bbtn):
    tutorialButton['background'] = '#CACACA'

def show_frame():
    frame = face.update_frame()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(frame)
    if (imageFrame['width']==WIDTH//2):
        img = img.resize((WIDTH//2,HEIGHT//2), Image.ANTIALIAS)
    else:
        img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    imageFrame.imgtk = imgtk
    imageFrame.config(image=imgtk)
    imageFrame.after(10, show_frame)
    direction.set(showDirection(face.get_direction()))


panelFrame = tk.Frame(root)
panelFrame.pack(side="bottom", fill="x")

panelButton = tk.Button(panelFrame, text="Start", command=startProcess, relief="flat", bg="#CACACA")
panelButton.pack(side="bottom", fill="x")

panelButton.bind("<Enter>", p_on_enter)
panelButton.bind("<Leave>", p_on_leave)

tutorialButton = tk.Button(panelFrame, text="Tutorial", command=openTutorial, relief="flat", bg="#CACACA")
tutorialButton.pack(side="bottom", fill="x")

tutorialButton.bind("<Enter>", t_on_enter)
tutorialButton.bind("<Leave>", t_on_leave)

direction = tk.StringVar()
faceDirectionLabel = tk.Label(panelFrame, textvariable=direction)
faceDirectionLabel.config(anchor="center")
faceDirectionLabel.pack(side="top", pady=10)

imageFrame = tk.Label(root)
imageFrame.pack(side="top")
orig_width = imageFrame['width']
orig_height = imageFrame['height']

show_frame()

root.mainloop()

face.release_camera()
