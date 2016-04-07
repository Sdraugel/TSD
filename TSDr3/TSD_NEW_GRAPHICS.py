from tkinter import *
from time import sleep

class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        # determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        # resize the canvas 
        #self.config(width=self.width, height=self.height)
        # rescale all the objects tagged with the "all" tag
        self.scale("all",0,0,wscale,wscale)


class wind:
    def __init__(self):
        self.root = Tk()
        #topFrame = Frame(root)

        self.machineName = StringVar()
        self.machineName.set('Test')
        self.theLabel = Label(self.root,textvariable =self.machineName )
        self.theLabel.pack(side = BOTTOM)
        
        self.canvas1 = ResizingCanvas(self.root,width = 1000, height = 500, bg = 'light grey')
        self.canvas1.pack(side = LEFT,expand=YES, fill=BOTH)
        self.circle1 = self.canvas1.create_oval(700,50,450,300,fill = 'red')
        self.circle2 = self.canvas1.create_oval(400,50,50,400,fill = 'red')
        
        
        self.root.update()

    def update(self,text):
        self.machineName.set('CHANGED IT')



    
    
        
test = wind()
sleep(1)
test.update('d')









