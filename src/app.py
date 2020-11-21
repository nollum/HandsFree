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

root = tk.Tk()
root.option_add('*Font', '19')
root.title("Auto-Scroller")
root.geometry("{}x{}".format(WIDTH, HEIGHT))
root.geometry('+{}+{}'.format(100,100))
root.resizable(False, False)
root.iconbitmap('../img/logo.ico')
root.option_add("*Font", ("Consolas", 20))

def showDirection(dir):
    if dir == 1:
        return 'Up'
    elif dir == 2:
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
        if face.get_direction() == 1:
            up()
        elif face.get_direction() == 2:
            down()
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