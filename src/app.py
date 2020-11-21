import tkinter as tk
from tkinter import font
import FaceTracker as ft
from PIL import Image, ImageTk
import cv2
import pyautogui
import time

#WINDOW
WIDTH = 600
HEIGHT = 600

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
    mouse_x, mouse_y = mouse.get_position()
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
#root.iconbitmap('../img/logo.ico')
root.option_add("*Font", ("Consolas", 20))

def showDirection(dir):
    if dir == 2:
        return 'Up'
    elif dir == 1:
        return 'Down'
    elif dir == 3:
        return 'No movement'
    else:
        return 'Not looking at camera'

def key_pressed(event):
    endProcess()

def endProcess():
    root.geometry("{}x{}".format(WIDTH, HEIGHT))
    root.attributes('-topmost', False)
    startFrame.pack(side="bottom", fill="x")
    imageFrame.config(width=orig_width, height=orig_height)

def startProcess():
    startFrame.pack_forget()
    root.geometry("{}x{}".format(WIDTH//2, HEIGHT//2))
    imageFrame.config(width=WIDTH//2, height=HEIGHT//2)
    root.attributes('-topmost', True)
    root.bind("<Key>", key_pressed)
    while imageFrame['width'] == WIDTH//2:
        nose_x, nose_y = face.get_nose_direction()
        if face.get_direction() == 2:
            up()
        elif face.get_direction() == 1: 
            down()
        elif abs(nose_x) > constants.diagonal_x_sens and abs(nose_y) > constants.diagonal_y_sens: #diagonal
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

def on_enter(event):
    startButton['background'] = 'grey'

def on_leave(event):
    startButton['background'] = '#CACACA'

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

imageFrame = tk.Label(root)
imageFrame.pack()
orig_width = imageFrame['width']
orig_height = imageFrame['height']

startFrame = tk.Frame(root)
startFrame.pack(side="bottom", fill="x")

startButton = tk.Button(startFrame, text="Start", command=startProcess, relief="flat", bg="#CACACA")
startButton.pack(side="bottom", fill="x")

startButton.bind("<Enter>", on_enter)
startButton.bind("<Leave>", on_leave)

direction = tk.StringVar()
faceDirection_lbl = tk.Label(startFrame, textvariable=direction)
faceDirection_lbl.config(anchor="center")
faceDirection_lbl.pack(side="top", pady=10)

show_frame()

root.mainloop()

face.release_camera()
