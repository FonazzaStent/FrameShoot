"""FrameShoot 1.0.o - An very simple frame-by-frame stop motion program
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


import tkinter
import cv2
import PIL.Image, PIL.ImageTk
from PIL import Image
import time
import os

def classes():
    global App
    class App:
        def __init__(self, window, window_title, video_source=0):
             self.window = window
             self.window.title(window_title)
             self.video_source = video_source
     
             # open video source (by default this will try to open the computer webcam)
             self.vid = MyVideoCapture(self.video_source)
     
             # Create a canvas that can fit the above video source size
             self.canvas = tkinter.Canvas(window, width = self.vid.width, height = self.vid.height)
             self.canvas.pack()
     
             # Button that lets the user take a snapshot
             self.btn_snapshot=tkinter.Button(window, text="Shoot frame", width=25, command=self.snapshot)
             self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
             self.btn_toggleonion=tkinter.Button(window,text="Onion Skin", width =25, command=self.toggle_onion)
             self.btn_toggleonion.pack(anchor=tkinter.CENTER, expand=True)     
             # After it is called once, the update method will be automatically called every delay milliseconds
             self.delay = 15
             self.update()
     
             self.window.mainloop()

        def toggle_onion(self):
             try:
                 global filename
                 global flag
                 if flag==0:
                     filename=""
                     flag=1
                 else:
                     filename=oldfilename
                     flag=0
             except:
                 True

        def snapshot(self):
             global filename
             global oldfilename
             global flag
             flag=0
             # Get a frame from the video source
             ret, frame = self.vid.get_frame()
     
             if ret:
                 filename=('./frames/frame-' + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg")
                 oldfilename=filename
                 imgdir="./frames"
                 if not os.path.exists(imgdir):
                     os.mkdir('frames')
                 cv2.imwrite(filename, cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
                 #print (filename)

                 
        def update(self):
             # Get a frame from the video source
             ret,background=self.vid.get_frame()
             #background1 = cv2.flip(background,1)
             try:
                 #print (filename)
                 foreground=cv2.imread(filename,cv2.IMREAD_COLOR)
                 added_image = cv2.addWeighted(background,1,foreground,0.4,0)
                 blend = added_image
                 self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(blend))
                 self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
             except:
                 #print ("error")
                 self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(background))
                 self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
                 
             #print(filename)
                 
             self.window.after(self.delay, self.update)
     
    class MyVideoCapture:
        def __init__(self, video_source=0):
            # Open the video source
            self.vid = cv2.VideoCapture(video_source)
            if not self.vid.isOpened():
                raise ValueError("Unable to open video source", video_source)

            # Get video source width and height
            self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
            self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

        def get_frame(self):
            if self.vid.isOpened():
                ret, frame = self.vid.read()
                if ret:
                    # Return a boolean success flag and the current frame converted to BGR
                    return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                else:
                    return (ret, None)
            else:
                return (ret, None)

        # Release the video source when the object is destroyed
        def __del__(self):
            if self.vid.isOpened():
                self.vid.release()


# Create a window and pass it to the Application object

classes()
App(tkinter.Tk(), "Frame Motion")
