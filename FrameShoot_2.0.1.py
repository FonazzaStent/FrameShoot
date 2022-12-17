"""FrameShoot 2.0.1 - A very simple frame-by-frame stop motion program
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

def init():
    global cap
    global lastframefile
    global lastframepath
    global lastframe
    global onion
    global quitcheck
    global fps
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
    onion=1
    imgdir="./frames"
    if not os.path.exists(imgdir):
        os.mkdir('frames')
    quitcheck=0
    fps=15
    
#Create app window
def appwindow():
    global top
    global root
    global canvas1
    global fpsentry
    global fpslabel1
    loop=0
    img="iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAKGHpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjarZhpliSrDYX/swovgUkMy2E8xzvw8v2JGCqr+rXdHjK7MgKCAKSreyXarH/8fZu/8fGlFhMll1RTsnxijdU3boq9Pv38OhvP7/n4+xHtb/3mfeDpClzD1azPg0U/9+5u13sR94x/JnpuXONOvh60dvf37/39ntCXnxPdOwjuWtnO+4V7ouDvHcWrPe4dpVryN9PmuFeOd1f5+osh+yTJ5chv9DbnVLkv3saMP6duNOTLbeZZ6el42s9Qz578Ci5YfkPw1y6D/vnQ6L9+BWfTWWn4UM5vvaABSrbAxPWaeDf7OvPTN18++s3nT8yyLLKXDv5A7b3+iJv3zv2m/w6DF7WS7gfhO6w2vde/7HfyTPQ8CO86/nPlMt6Vv/X3beunK8wn3HvPso/RWNFiwhfpNuox5dwxrqsXz1uJb7bJELWFG/1WvsU2OwiBaQdM69xX58F+u+ima267da7DDbYY/fKZq/fD+HA6CyBVPwgFF6J+3faZsJgEhQ/jxFAM/t2LO8vWs9xwxU5jp2Ood0zmTpD9l1/zpwP3Vi45Z8vrK/blNdLZhXXArxeGgYjbt1PlOPj5/vworgEE5bi5YGCz3VxTdHFfwRUO0IGBwvXinsvzngAXsbSwGRdAwCaI5hI7yt5n53BkAaDG1n2IvoOAE/GTTfoYQgIc2MHavJPdGerFX92oaogmSEghgw3EBawYhfjJsRBDTYJEEUmSpUiVlkJS5qWUk8pzyyHHLDnlnIvJNbcSSixSUsmloOOt+hqQb6nwtJZaa2ss2pi58XZjQGvd99Bjl5567qVX09sgfEYcMtLIo4w62vQzTAg+08yzzDrbcotQWnHJSiuvsupqm1DbYcctO+1sdtl1txe1G9Zfvv8Bau5GzR+kdGB+UaM352cKp3IiihmI+egAPIMaiBHYipktLkavyClm5CNYIZ5NioIznSIGgnE5L9u92N3IGbz4f8HN5HJw8/8rckah+0PkfsXtr1CbmiXGQeyioTrVBtjH89VnT+xkrDZJPt0VJsx+TEnNF3bmihEX+QcxinZpKn6v0jQvfz6o6UfH19UAoc6kmbCdLuvIaOfGtp7hG4MRXUHaZA2RjLPE9YqiSikUL60HkWYayVxn2DJaBacRysAJYctsk3miKKTNj6wA5jgBU8bbxNdX06Cgn22aXabXPZ5m1SYxF4u2uo7NWJAtsbaImw6OvvQipqwElqsq3vNeSaea97tZ363Pu1Uy6oKFkQgjuGMeQ0e0ZmauBNxgkqGmW53G6U/0PrYGLql1gRlcJvCNyjWt7moPGcAsu0SZpok1MYEsQoa9+l7c2lXrQacGZhvmJoT7sKk0ONo3r/GQV7+NddSQw+48mmfsAqzF4DX99TR+PMP0M3T+GKqb6LJMD4zWiMFrJHTJYwfZEIx9T4nwEke4HndLElbPCHpSiwl7vOjqqszUspgFJxdegGkLlumWFaMWWLXDMKgA3ayb8fh5x4BXyQQ2kxVzZ+XSIVEyWdCVMCZuRPNX721XT+HMqw00PBOwEHsrcAV2Uo2pedsmws66NQUP51aNDkTDhu6wBBn09jEjaocrcOiCwNt1itzgoNxWv3Ndq1B0Kic6roltG5faxujtpLVStQCcTfMLZmuA16CkOCTQ9ctme9Dlhz+Y0Vz+gF/Au4JvkWoRCwZWojgrUQYTh3hBkAuPtZkAKInMMTEjY0YGzGmNImphmsM3EReF1rALz8nCtxoHYYpnFArFHsASnwjxNRYWztZHgNu+GdI8S8xcFoIKMNCy29A9LsVgm7lqJCqY/gQWrpPUZ2PXeKP5OMoKqZqjGXOsdMnU7Y2xI77jdntgFERB6kTpjkbhw3KWCIgGntlYUYyGfVKOVI1Cgl71KbcMbYkVIkbjTfXqaVTmX+r4fA2Ua6Apco+kCsHDusZWVQuQ+A4txLkCbiJKmiMIh+SaNHZ451JDjkxGI5PQiVOvEmOtbqSpLkEVex2DCysduylLpgYT3B7kELoQASjpAN2oDl9GV4wlZCPRFVYrKUAtVS380imI/Ak+a4ERvbJTU58lGyyfOiFqpBWVg8o+j3Rf4SrhiLwcJivbwYn4KlCbwAasRRQhKVsrACKNODqg1hvW9glrVFiZiw1vjCy4Cbcg5Q2rrVp5WXdZaR4z7VmeyCbOkWIyAqu1xUmSHL9J2WzTT6H2iGdtq8YmmdlnSFezUSZRl9RDpa4eHprp8YYLM5FIvJM+abGPo6kIEkQZjJ2qIQRZt34jtSrmHWMi/JlQKUhRuChB7KHyQ+leOAMopYkcUVow45xQq7M8MuJtyhQkWXnEMQxezKSnQorWY4OihaZCeCW+O1elXvcqeADSNJZqMvXk1l5iW7AQGlUic4JSAtljSRgZzApq4NWPTJpvYK2WhFCIgEVq9UXv6wG7KIO1vhDGAM+khEt3iie8jnbVc+2vdlFG4OFu0K5R17/A9RPWh7BBKxrIjBf9JHZtnqZqGkagnApuK0pLmYd5E6IhQYh00gQ5UQWlhm6eVjrxXJxmB9rdqN0a5QS7Pl9HGKlCgAKXVkJqdoDRnLBx77C65kLaDwK7XwHlojk++7T+S7mJRbU+YXxnw0eg9JDxQV2Kv4muupQNxedVQp2YptgZKPbkrdC0rNoq4213CIzLSidqNdsHlRdeUQlkXcTHoO99xdD0P1m25t7ZT7WBglNqsJMFN6eKdT2h0LUGmBq3LlEo8nK54L8yF+Ehql+J5sRUGJ6oKmxTP5B+rBx/jK9676Z409BTipvxxfGpQraEZEgWIJGKf5VMYyE9saDC+eENrxHejVP9xaZ55DNhSlI6r+A0kcFOzWgUzl5DulPyo0RTHwYvVrOUvRYyA2smhUKxSmkGcCwPS7Mi0lyUfHuSxVQNcToURJnaiieWersMJNqGEaCBxVpBXfXFPgEhV+D9JjJUujBHWaFCn+ATCtlOmVPmyeZvVh8nq/dTPh4F4Cgy2FyvV6IqWmfS0hrIbjsM9RfpUYHYdl6NwwFMz0/drSXFybJYN0aD8Ge801oOWTgN860FfjvWn5X+h5ivJ0drmJaFjbzKWUKII5RWIrxD3/A3GkTxR+RsTiEYqGC7Oa6zAH4Zvv5yPjhX89xcOncJz9Gm++Zr6Hn3qOKPsafDXKjwVyeSaAvlxBopz6vcJkZd0WILkXYn5wd7FxcYyYNMXuaQsao5xW86hdFQ0Z4hdIcDOJmx1giglLRK8qqvyWqTFSi9ENvil+YbHgoy4qn2SS5asOG/lu/BYMvj371bf2maX6b+fBeaOxcnhw6OVKuoAKmEa/4ZnLB531/lRV2G86rDB1Ro1MNbC4pCpLDHkDxnaApjPNK9fSqBeB/v7MdVaxfz3t037tHO72P/7RWuJRhCpt0cC9iWEkorveg5723OutVa809UcMMZ/t49KgAAAYRpQ0NQSUNDIHByb2ZpbGUAAHicfZE9SMNAHMVfU6VFKh3sINIhQ3WyICriKFUsgoXSVmjVweTSL2jSkKS4OAquBQc/FqsOLs66OrgKguAHiKOTk6KLlPi/pNAixoPjfry797h7BwitGlPNvglA1Swjk0yI+cKqGHhFCGEEEUVQYqaeyi7m4Dm+7uHj612cZ3mf+3MMKkWTAT6ReI7phkW8QTyzaemc94kjrCIpxOfE4wZdkPiR67LLb5zLDgs8M2LkMvPEEWKx3MNyD7OKoRJPE8cUVaN8Ie+ywnmLs1prsM49+QtDRW0ly3WaUSSxhBTSECGjgSpqsBCnVSPFRIb2Ex7+EcefJpdMrioYORZQhwrJ8YP/we9uzdLUpJsUSgD9L7b9MQoEdoF207a/j227fQL4n4Erreuvt4DZT9KbXS12BIS3gYvrribvAZc7wPCTLhmSI/lpCqUS8H5G31QAhm6BgTW3t84+Th+AHHW1fAMcHAJjZcpe93h3sLe3f890+vsBQPtyk1sQQYAAAA12aVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/Pgo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA0LjQuMC1FeGl2MiI+CiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiCiAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICB4bWxuczpHSU1QPSJodHRwOi8vd3d3LmdpbXAub3JnL3htcC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgeG1wTU06RG9jdW1lbnRJRD0iZ2ltcDpkb2NpZDpnaW1wOjAxNjk2ZDI5LTJjNDQtNDhjMS04NmY1LTcyY2VlMzI3NTJjMSIKICAgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDpkMDMzYmExNS0zMGY2LTQ3N2UtYWJkYi01OGU2NWU3MWYxMGMiCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDo4NTVlZTk1Mi02ZTA0LTQ1NjItOTY4My04ODliYzdmZWY3MGYiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICBHSU1QOkFQST0iMi4wIgogICBHSU1QOlBsYXRmb3JtPSJXaW5kb3dzIgogICBHSU1QOlRpbWVTdGFtcD0iMTY3MTA5MjkxMTk0MzI4MiIKICAgR0lNUDpWZXJzaW9uPSIyLjEwLjMyIgogICB0aWZmOk9yaWVudGF0aW9uPSIxIgogICB4bXA6Q3JlYXRvclRvb2w9IkdJTVAgMi4xMCIKICAgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyMjoxMjoxNVQwOToyODoyOSswMTowMCIKICAgeG1wOk1vZGlmeURhdGU9IjIwMjI6MTI6MTVUMDk6Mjg6MjkrMDE6MDAiPgogICA8eG1wTU06SGlzdG9yeT4KICAgIDxyZGY6U2VxPgogICAgIDxyZGY6bGkKICAgICAgc3RFdnQ6YWN0aW9uPSJzYXZlZCIKICAgICAgc3RFdnQ6Y2hhbmdlZD0iLyIKICAgICAgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo0ZGNkNmVkYi1jZTg1LTRmMWUtYTU3ZC1kOWM4ZmI3Y2I4Y2UiCiAgICAgIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkdpbXAgMi4xMCAoV2luZG93cykiCiAgICAgIHN0RXZ0OndoZW49IjIwMjItMTItMTVUMDk6Mjg6MzEiLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b3J5PgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAg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"
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
    fpslabel.place(x=230,y=510,height=30,width=200)
    fpslabel1=tk.Label(text="15")
    fpslabel1.place(x=405,y=510,height=30,width=20)    
    fpsentry=tk.Entry(top, textvariable=fps)
    fpsentry.place(x=430,y=510,height=30,width=40)
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
    video_button=tk.Button(top)
    video_button.place(x=20,y=510,height=30,width=80)
    video_button.configure(text="Shoot Frame")
    video_button.bind("<Button-1>",shoot_event)
    onion_button=tk.Button(top)
    onion_button.place(x=115,y=510,height=30,width=120)
    onion_button.configure(text="Toggle Onion Skin")
    onion_button.bind("<Button-1>",toggle_onion)
    setfps=tk.Button(text="Set")
    setfps.place(x=475,y=510,height=30,width=30)
    setfps.bind("<Button-1>",set_fps)

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
    while True and quitcheck==0:
        if lastframe=="" or onion==0:
            root.delay=100
            ret,frame= cap.read()
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
    filename=('./frames/frame-' + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg")
    imgdir="./frames"
    if not os.path.exists(imgdir):
     os.mkdir('frames')
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
    
def main():
    init()
    appwindow()
    create_buttons()
    create_menu()
    display()

main()
root.mainloop()
