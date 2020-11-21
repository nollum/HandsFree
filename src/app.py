import tkinter as tk
from tkinter import font
import FaceTracker as ft
from PIL import Image, ImageTk
import cv2, pyautogui, time, webbrowser

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
    pyautogui.moveRel(n*20, m*20, 0.1) #scroll down by n (-n)

#Click the mouse at current position
def click():
    pyautogui.click() #by default, this left-clicks at the current (x, y) cursor position

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
    faceDirectionLabel.config(anchor="center")
    faceDirectionLabel.pack(side="top", pady=10)
    panelButton.config(text="Start")
    panelButton.config(command=startProcess)
    panelButton.pack(side="bottom", fill="x")
    panelFrame.pack(side="bottom", fill="x")
    imageFrame.config(width=orig_width, height=orig_height)

def startProcess():
    faceDirectionLabel.forget()
    panelButton.config(text="Stop")
    panelButton.config(command=endProcess)
    root.geometry("{}x{}".format(WIDTH//2, HEIGHT//2))
    imageFrame.config(width=WIDTH//2, height=HEIGHT//2)
    root.attributes('-topmost', True)
    root.bind("<Key>", key_pressed)
    while imageFrame['width'] == WIDTH//2:
        if face.get_direction() == 1:
            up()
        elif face.get_direction() == 2:
            down()
        nose_x, nose_y = face.get_nose_direction()
        print(nose_x)
        if nose_x > 10 and nose_y > 10:
            move_mouse(nose_x, nose_y)
        elif nose_x > 10:
            move_mouse(nose_x, 0)
        elif nose_y > 10:
            move_mouse(0, nose_y)
        root.update()

def on_enter(event):
    panelButton['background'] = 'grey'

def on_leave(event):
    panelButton['background'] = '#CACACA'

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

imageFrame = tk.Label(root)
imageFrame.pack(side="top")
orig_width = imageFrame['width']
orig_height = imageFrame['height']

panelButton = tk.Button(panelFrame, text="Start", command=startProcess, relief="flat", bg="#CACACA")
panelButton.pack(side="bottom", fill="x")

panelButton.bind("<Enter>", on_enter)
panelButton.bind("<Leave>", on_leave)

direction = tk.StringVar()
faceDirectionLabel = tk.Label(panelFrame, textvariable=direction)
faceDirectionLabel.config(anchor="center")
faceDirectionLabel.pack(side="top", pady=10)

show_frame()

root.mainloop()

face.release_camera()
