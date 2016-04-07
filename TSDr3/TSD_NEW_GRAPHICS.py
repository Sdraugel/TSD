from tkinter import *
from win32api import GetSystemMetrics
import time

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
        
    def create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)


class TSD_Graphics:

    def __init__(self,root,canvas,machine,lastPass,x,y):
        #topFrame = Frame(root)

##        self.machineName = StringVar()
##        self.machineName.set('Test')
##        self.theLabel = Label(self.root,textvariable =self.machineName )
##        self.theLabel.pack(side = BOTTOM)
##        
##        self.canvas1 = ResizingCanvas(self.root,width = 1000, height = 500, bg = 'light grey')
##        self.canvas1.pack(side = LEFT,expand=YES, fill=BOTH)
##        self.circle1 = self.canvas1.create_oval(700,50,450,300,fill = 'red')
##        self.circle2 = self.canvas1.create_oval(400,50,50,400,fill = 'red')
##        
##        
##        self.root.update()
        self.root = root
        self.canvas = canvas
        self.machine = machine
        self.x = x
        self.y = y
        self.val = 0
        self.count = 1
        self.totalPass = 0
        self.totalFail = 0
        self.start = time.time()

 
        
        self.valArr = []
        for i in range(0,199): ##initialize array holding values past 100 values (queue-like structure)
            self.valArr.append(0)
            
        self.barArr = [] ##array containing rectangle objects
        for i in range(0,199):
            self.barArr.append(self.canvas.create_line(i*2+self.x,self.y,(i+1)*2+self.x,self.val+self.y)) ##initialize array containing rectangle objects

        self.circle = self.canvas.create_circle(155+self.x,200+self.y,150,fill = 'white')

        self.currentRuns = self.canvas.create_text(155+self.x,190 +self.y,text = "Initializing...",font = ("system",int(GetSystemMetrics(0)/40)))

    def update(self,text):
        self.machineName.set('CHANGED IT')


def getColor(var):
    if (Debug == 1):
        print("Set colors")
        
    if var < THRESHOLD_FAIL_PERCENTAGE:
        color = 'red'
    elif var < THRESHOLD_WARNING_PERCENTAGE:
        color = 'yellow'
    else:
        color = 'green'
    return color

root = Tk()
canvas = ResizingCanvas(root,width = 1000, height = 560, bg = 'light grey')
canvas.pack(side = LEFT,expand=YES, fill=BOTH)

tsd = TSD_Graphics(root,canvas,'machine1','hello',0,0)
tsd = TSD_Graphics(root,canvas,'machine1','hello',500,0)




    
    










