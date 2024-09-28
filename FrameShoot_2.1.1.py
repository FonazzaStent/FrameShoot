"""FrameShoot 2.1.1 - A very simple frame-by-frame stop motion program
to create animations with your webcam.
Copyright (C) 2022  Fonazza-Stent

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>."""


import sys
import tkinter as tk
import tkinter.ttk as ttk
from tkinter.constants import *
from tkinter import *
from tkinter import messagebox
import cv2
import PIL.Image, PIL.ImageTk
import time
import os
import glob
from PIL import Image
from tkinter.filedialog import asksaveasfilename
from tkinter.filedialog import askopenfilename
import shutil
import webbrowser

try:
    import pyi_splash
    pyi_splash.close()
except:
    True

def init():
    global cap
    global lastframefile
    global lastframepath
    global lastframe
    global firstframe
    global firstframepath
    global firstframe
    global onion
    global quitcheck
    global fps
    global flip
    global firstframecheck
    global onionskin
    cap=cv2.VideoCapture(0)
    lastframepath="./lastframe.txt"
    if os.path.exists("./frames/lastframe.txt"):
        shutil.copyfile("./frames/lastframe.txt","./lastframe.txt")
    if not os.path.exists(lastframepath):
        lastframefile=open(lastframepath,'w')
        lastframefile.close()
    lastframefile=open(lastframepath,'r')
    lastframe=lastframefile.read()
    lastframefile.close()
    if not os.path.exists(lastframe):
        lastframe=""
    imgdir="./frames"
    if not os.path.exists(imgdir):
        os.mkdir('frames')
    firstframepath="./frames/firstframe.txt"   
    if not os.path.exists(firstframepath):
        firstframefile=open(firstframepath,'w')
        firstframefile.close()
    firstframefile=open(firstframepath,'r')
    firstframe=firstframefile.read()
    firstframefile.close()
    if not os.path.exists(firstframe):
        firstframe=""
        
    onion=1

    quitcheck=0
    fps=15
    flip=False
    firstframecheck=False
    onionskin="last"
    
#Create app window
def appwindow():
    global top
    global root
    global canvas1
    global fpsentry
    global fpslabel1
    loop=0
    img="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Z2ltcDpkb2NpZDpnaW1wOjAxNjk2ZDI5LTJjNDQtNDhjMS04NmY1LTcyY2VlMzI3NTJjMSIKICAgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpkMDMzYmExNS0zMGY2LTQ3N2UtYWJkYi01OGU2NWU3MWYxMGMiCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDo4NTVlZTk1Mi02ZTA0LTQ1NjItOTY4My04ODliYzdmZWY3MGYiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICBHSU1QOkFQST0iMi4wIgogICBHSU1QOlBsYXRmb3JtPSJXaW5kb3dzIgogICBHSU1QOlRpbWVTdGFtcD0iMTY3MTA5MjkxMTk0MzI4MiIKICAgR0lNUDpWZXJzaW9uPSIyLjEwLjMyIgogICB0aWZmOk9yaWVudGF0aW9uPSIxIgogICB4bXA6Q3JlYXRvclRvb2w9IkdJTVAgMi4xMCIKICAgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMjoxMjoxNVQwOToyODoyOSswMTowMCIKICAgeG1wOk1vZGlmeURhdGU9IjIwMjI6MTI6MTVUMDk6Mjg6MjkrMDE6MDAiPgogICA8eG1wTU06SGlzdG9yeT4KICAgIDxyZGY6U2VxPgogICAgIDxyZGY6bGkKICAgICAgc3RFdnQ6YWN0aW9uPSJzYXZlZCIKICAgICAgc3RFdnQ6Y2hhbmdlZD0iLyIKICAgICAgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo0ZGNkNmVkYi1jZTg1LTRmMWUtYTU3ZC1kOWM4ZmI3Y2I4Y2UiCiAgICAgIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkdpbXAgMi4xMCAoV2luZG93cykiCiAgICAgIHN0RXZ0OndoZW49IjIwMjItMTItMTVUMDk6Mjg6MzEiLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b3J5PgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg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"
    root= tk.Tk()
    top= root
    top.geometry("680x560")
    top.resizable(0,0)
    top.title("FrameShoot")
    favicon=tk.PhotoImage(data=img) 
    root.wm_iconphoto(True, favicon)
    canvas1=tk.Canvas(top, width=640, height=480)
    canvas1.place(x=20,y=20)
    root.protocol("WM_DELETE_WINDOW", on_closing)
    fpslabel=tk.Label(text="Frames per second (1 to 60)=")
    fpslabel.place(x=375,y=510,height=30,width=200)
    fpslabel1=tk.Label(text="15")
    fpslabel1.place(x=550,y=510,height=30,width=20)    
    fpsentry=tk.Entry(top, textvariable=fps)
    fpsentry.place(x=575,y=510,height=30,width=40)
    fpsentry.bind("<Return>",set_fps)


#set fps
def set_fps(event):
    global fps
    entryvalue=fpsentry.get()
    if entryvalue.isdigit()==True:
            fps=int(entryvalue)
            if fps<1:
                    fps=1
            if fps>60:
                    fps=60
    fpslabel1.configure(text=fps)
    fpsentry.delete(0,END)
    
#Create buttons
def create_buttons():
    global video_button
    global toggle_onion
    global setfps
    global firstlast
    global flip_button
    video_button=tk.Button(top)
    video_button.place(x=20,y=510,height=30,width=80)
    video_button.configure(text="Shoot Frame")
    video_button.bind("<Button-1>",shoot_event)
    onion_button=tk.Button(top)
    onion_button.place(x=105,y=510,height=30,width=120)
    onion_button.configure(text="Toggle Onion Skin")
    onion_button.bind("<Button-1>",toggle_onion)
    setfps=tk.Button(text="Set")
    setfps.place(x=625,y=510,height=30,width=30)
    setfps.bind("<Button-1>",set_fps)
    firstlast=tk.Button(top)
    firstlast.place(x=230,y=510,height=30,width=60)
    firstlast.configure(text="First/Last")
    firstlast.bind("<Button-1>",firstlast_function)
    flip_button=tk.Button(top)
    flip_button.place(x=295,y=510,height=30,width=40)
    flip_button.configure(text="Flip")
    flip_button.bind("<Button-1>",flip_function)

#Create menu
def create_menu():
    menubar=tk.Menu(top, tearoff=0)
    top.configure(menu=menubar)
    sub_menu=tk.Menu(top, tearoff=0)
    menubar.add_cascade(menu=sub_menu,compound="left", label="File")
    sub_menu.add_command(compound="left",label="Preview", command=preview, accelerator="Alt+P")
    sub_menu.add_command(compound="left",label="Export to AVI", command=avi,accelerator="Alt+A")
    sub_menu.add_command(compound="left",label="Export to GIF", command=gif, accelerator="Alt+G")
    sub_menu.add_command(compound="left",label="Quit", command=QuitApp, accelerator="Alt+Q")
    top.bind_all("<Alt-p>",preview_hotkey)
    top.bind_all("<Alt-a>",avi_hotkey)
    top.bind_all("<Alt-g>",gif_hotkey)
    top.bind_all("<Alt-q>",QuitApp_hotkey)
    menubar.bind_all("<Alt-f>",menubar.invoke(1))

    #About menu
    about=tk.Menu(top, tearoff=0)
    menubar.add_cascade(menu=about,compound="left", label="?")
    about.add_command(compound="left", label="Help", command=helpbox)
    about.add_command(compound="left", label="About", command=aboutbox)

#firstlast_function
def firstlast_function(event):
    global lastframe
    global onionskin
    if onionskin=="last":
        if os.path.exists("./frames/firstframe.txt"):
            lastframefile=open("./frames/firstframe.txt",'r')
            lastframe=lastframefile.read()
            lastframefile.close()
            firstlast.configure(text="First")
            onionskin="first"
    else:
        if onionskin=="first":
            if os.path.exists("./frames/lastframe.txt"):
                lastframefile=open("./frames/lastframe.txt",'r')
                lastframe=lastframefile.read()
                lastframefile.close()
                firstlast.configure(text="Last")
                onionskin="last"

#flip
def flip_function(event):
    global flip
    if flip==False:
        flip=True
    else:
        flip=False

#export to GIF
def gif():
    global fps
    mms=1000/fps
    data=[('Animated GIF','*.gif')]
    giffilename=asksaveasfilename(filetypes=data, defaultextension=data)
    if str(giffilename)!='':
        frames = [Image.open(image) for image in glob.glob(f"./frames/*.JPG")]
        frame_one = frames[0]
        frame_one.save(giffilename, format="GIF", append_images=frames,
                   save_all=True, duration=mms, loop=0)
def gif_hotkey(event):
    gif()
    
#export to AVI
def avi():
    data=[('AVI Video','*.avi')]
    avifilename=asksaveasfilename(filetypes=data, defaultextension=data)
    if str(avifilename)!='':
        img_array = []
        for framefile in glob.glob('./frames/*.jpg'):
            img = cv2.imread(framefile)
            img_array.append(img)
        size=(640,480)
        out = cv2.VideoWriter(avifilename,0, fps, size)
        for i in range(len(img_array)):
            out.write(img_array[i])
        out.release()
def avi_hotkey(event):
    avi()


#Quit
def QuitApp():
    okcancel= messagebox.askokcancel("Quit?","Do you want to quit the app?",default="ok")
    if okcancel== True:
        on_closing()
def QuitApp_hotkey(event):
    QuitApp()

#Create display
def display():
    global frame1
    global lastframe
    global quitcheck
    global flip
    while True and quitcheck==0:
        if lastframe=="" or onion==0:
            root.delay=100
            ret,frame= cap.read()
            if flip==True:
                frame = cv2.flip(frame,-1)
            frame1=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img=PIL.Image.fromarray(frame1)
            newsize=(640,480)
            img1=img.resize(newsize)
            img2 = PIL.ImageTk.PhotoImage(image = img1)
            canvas1.create_image(0, 0, image = img2, anchor = tk.NW)
            canvas1.update()
            root.after(root.delay,root.update)
        else:
            root.delay=100
            ret,frame= cap.read()
            if flip==True:
                frame = cv2.flip(frame,-1)
            frame1=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            foreground=cv2.imread(lastframe,cv2.IMREAD_COLOR)
            blend=cv2.addWeighted(frame1,1,foreground,0.5,0)
            img=PIL.Image.fromarray(blend)
            newsize=(640,480)
            img1=img.resize(newsize)
            img2 = PIL.ImageTk.PhotoImage(image = img1)
            canvas1.create_image(0, 0, image = img2, anchor = tk.NW)
            canvas1.update()
            root.after(root.delay,root.update)
            
def shoot_event(event):
    shoot_frame()
    
def shoot_frame():
    global lastframefile
    global lastframe
    global firstframecheck
    filename=('./frames/frame-' + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg")
    imgdir="./frames"
    if not os.path.exists(imgdir):
     os.mkdir('frames')
    if firstframecheck==False:
        firstframefile=open(firstframepath,'w')
        firstframefile.write(filename)
        firstframefile.close()
        firstframefile=open(firstframepath,'r')
        firstframe=firstframefile.read()
        firstframefile.close()
        firstframecheck=True
        
    cv2.imwrite(filename, cv2.cvtColor(frame1, cv2.COLOR_RGB2BGR))
        
    lastframefile=open(lastframepath,'w')
    lastframefile.write(filename)
    lastframefile.close()
    lastframefile=open(lastframepath,'r')
    lastframe=lastframefile.read()
    lastframefile.close()
    shutil.copyfile("lastframe.txt","./frames/lastframe.txt")

def toggle_onion(event):
    global onion
    if onion==0:
        onion=1
    else:
        onion=0

#Preview
def preview_hotkey(event):
    preview()
    
def preview():
    img_array = []
    for framefile in glob.glob('./frames/*.jpg'):
        img = cv2.imread(framefile)
        img_array.append(img)
    size=(640,480)
    out = cv2.VideoWriter('preview.avi',0, fps, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()
    os.system("preview.avi")
    
def on_closing():
    global quitcheck
    quitcheck=1
    cap.release()
    lastframefile.close()
    root.destroy()

#About
def aboutbox():
    global aboutbox
    #print ('about')
    aboutbox=tk.Toplevel(top)
    aboutbox.geometry("500x240")
    aboutbox.resizable(0,0)
    aboutbox.title("About")
    about_label=Label(aboutbox)
    logo=b'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'
    logoimg=tk.PhotoImage(data=logo)
    about_label.place(x=35,y=40,height=102,width=430)
    about_label.configure(image=logoimg)
    about_label.image=logoimg
    about_label.bind("<Button-1>", lambda e: callback("https://fonazzastent.com/"))

    url_title=Label(aboutbox)
    url_title.place(x=35,y=10,height=40,width=430)
    url_title.configure(text="FrameShoot 2.1.1", font=("Arial",15), anchor='center')

    url_label=Label(aboutbox)
    url_label.place(x=35,y=152,height=15,width=430)
    url_label.configure(text="https://fonazzastent.com/", anchor='center')
    url_label.bind("<Button-1>", lambda e: callback("https://fonazzastent.com/"))

    url_label2=Label(aboutbox)
    url_label2.place(x=35,y=172,height=30,width=430)
    url_label2.configure(text="https://fonazzastent.com/frameshoot/", anchor='center')
    url_label2.bind("<Button-1>", lambda e: callback("https://fonazzastent.com/frameshoot/"))

    close_button=Button(aboutbox)
    close_button.place(x=220,y=200,height=30,width=40)
    close_button.configure(text="Close")
    close_button.bind("<Button-1>", close_aboutbox)
    
def close_aboutbox(event):
    aboutbox.destroy()

def callback(url):
    webbrowser.open_new_tab(url)

def helpbox():
    global helpbox
    helpbox=tk.Toplevel(top)
    helpbox.geometry("440x540")
    helpbox.resizable(0,0)
    helpbox.title("Help")
    
    textbox1 = Text(helpbox)
    textbox1.place(x=20, y=20, height=470, width=400)
    scroll_2=Scrollbar (helpbox)
    scroll_2.place(x=421, y=20, height=470, anchor='n')
    textbox1.configure(yscrollcommand=scroll_2.set, wrap=WORD)
    scroll_2.configure(command=textbox1.yview)
    textbox1.focus_set()
    readme="FrameShoot 2.1.1\n\
Fonazza-Stent\n\
\n\
A very simple program to create traditional photo animations with your \
webcam.\n\
The program consists of a webcam screen and a simple interface to take \
snapshots and save them to a folder in JPG format. You can create frame-\
by-frame photographic stop-motion animations by taking sequential shots \
of objects or drawings. The program is provided with an onion skin \
feature to give you a reference of the previous frame and help you \
arrange the new frame or create the next drawing. All the shots will be \
saved to a folder named \"frames\". You can use the built-in AVI and GIF \
generation functions or load all the frames into a video editing program \
to generate a video or into a photo editing program to create an \
animated GIF.\n\
\n\
Instructions:\n\
- unzip the ZIP archive to a folder\n\
- place your webcam in front or over the scene or drawing you want to \
Animate\n\
- click on \"Shoot frame\" to take the first frame \
- the frame will automatically be overlayed in transparency as onion skin\n\
- click on \"Toggle onion skin\" to toggle onion skin on and off\n\
- click on \"First/last frame\" to overlay as onion skin the first or the \
last frame (useful for looped GIFs)\n\
- Click on \"Flip\" to flip the frame horizontally and vertically\n\
- File-Preview (Alt-P) to preview the animation with your default video \
Player\n\
- File-Export to AVI (Alt-A) to export the animation to an AVI format \
Video\n\
- File-Export to GIF (Alt-G) to export the animation to an animated GIF\n\
- Set the framerate by typing a value in the \"Frames per second\" field + \
Enter or click on \"Set\"\n\
\n\
- The program will remember last onion skin frame when you open it \
- if you want to work on more than one project at a time, you can rename \
the \"frames\" folder to your project name and start a new project. To work \
on a project you put on hold through this procedure, rename the folder \
back to \"frames\". You can also store the project in another folder and \
copy it back to the main program folder when you want to work on it. Just \
remember to rename the project folder \"frames\"."
    textbox1.insert(INSERT,readme)
    textbox1.configure(state=DISABLED)
    close_button1=Button(helpbox)
    close_button1.place(x=200,y=500,height=30,width=40)
    close_button1.configure(text="Close")
    close_button1.bind("<Button-1>", close_helpbox)

def close_helpbox(event):
    helpbox.destroy()
   
def main():
    init()
    appwindow()
    create_buttons()
    create_menu()
    display()

main()
root.mainloop()
