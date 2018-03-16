#-*- coding: UTF-8 -*-
from Tkinter import *

class Application(Frame):

    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.pack()
        self.createWidgets()
        self.device_list=[]


    def createWidgets(self):
        self.add_button=Button(self,text="添加设备",command=self.add_device)
        self.add_button.pack()


    def add_device(self):
        deviceInput=Entry(self)
        deviceInput.pack()

app=Application()
app.master.title="test"
app.mainloop()
