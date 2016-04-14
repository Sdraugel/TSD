from tkinter import *
from tkinter.ttk import *
from win32api import GetSystemMetrics
import time
from time import sleep
from random import randint


THRESHOLD_FAIL_PERCENTAGE = 94
THRESHOLD_WARNING_PERCENTAGE = 97
EMAIL_62 = 0
EMAIL_64 = 0
WARNING_COUNT = 0
Debug = 0



class ResizingCanvas(Canvas):
    def __init__(self,parent,**kwargs):
        Canvas.__init__(self,parent,**kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self,event):
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height
        self.width = event.width
        self.height = event.height
        self.scale("all",0,0,wscale,wscale)
        
    def create_circle(self, x, y, r, **kwargs):
        return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)

def graphics_init():
    root = Tk()
    root.title("Test Stand Diagnostics")
    menubar = Menu(root)
    menubar.add_command(label="File")
    menubar.add_command(label="Edit")
    menubar.add_command(label="Run")
    menubar.add_command(label="Options")
    root.config(menu=menubar)
    lCanvas= ResizingCanvas(root,width = GetSystemMetrics(0), height = GetSystemMetrics(1)/6, bg = 'black')
    lCanvas.pack(side =BOTTOM,expand=NO, fill=BOTH)
    frame = Frame(root,height = 50)
    frame.pack(side = BOTTOM,expand = False)
    cCanvas = ResizingCanvas(root,width = 1000, height = 500, bg = 'light grey')
    cCanvas.pack(side = LEFT,expand=YES, fill=BOTH)

    return [root,menubar,cCanvas,lCanvas,frame]

class TSD_Graphics:

    def __init__(self,graphics_init_array,lineName,currPart,lastPart,xOffset,yOffset):
        
        self.root = graphics_init_array[0]
        self.menubar = graphics_init_array[1]
        self.cCanvas = graphics_init_array[2]
        self.lCanvas = graphics_init_array[3]
        self.failFrame = graphics_init_array[4]
        self.lineName = lineName
        self.currPart = currPart
        self.x = xOffset
        self.y = yOffset
        self.val = 0
        self.count = 1
        self.totalPass = 0
        self.totalFail = 0
        self.startTime = time.time()

        self.fontSize = 12

        last = lastPart.splitlines()
        
        self.valArr = []
        for i in range(0,199):
            self.valArr.append(0)
            
        self.lineArr = [] 
        for i in range(0,199):
            self.lineArr.append(self.lCanvas.create_line(i*2+self.x,self.y,(i+1)*2+self.x,self.val+self.y,fill = 'red')) 

        self.circle1 = self.cCanvas.create_circle(155+self.x,190+self.y,150,fill = 'white')
        self.circle2 = self.cCanvas.create_circle(400+self.x, 280+self.y,60,fill = getColor(float(last[2])))

        self.firstPassLabel = self.cCanvas.create_text(380 + self.x, 100 + self.y, text = "   Current Run" + "\nPart:      " + self.currPart + "\nCount:   " +str(self.count) + "\nUptime: " + timeElapsed(self.startTime),font = ("arial",self.fontSize))
        self.failList = Treeview(self.failFrame,height = 5)
        self.failList["columns"] = ("one","two")
        self.failList.column("#0",minwidth = 0, width = int(GetSystemMetrics(0)/10), stretch=NO)
        self.failList.column("one",minwidth = 0, width = int(GetSystemMetrics(0)/5), stretch=NO)
        self.failList.column("two",minwidth = 0, width = int(GetSystemMetrics(0)/5), stretch=NO)
        self.failList.heading("#0",text="Time")
        self.failList.heading("one",text="Failure")
        self.failList.heading("two",text="Solution")
        self.failList.insert("",0, text="13:30:05", values=("it not working","is it plugged in?"))
        self.failList.pack(side = LEFT)


        self.percentDraw = self.cCanvas.create_text(155+self.x,190 +self.y,text = "Initializing...",font = ("system",int(GetSystemMetrics(0)/40)))
        self.lineNameDraw = self.cCanvas.create_text(155+self.x,25 +self.y,text = self.lineName + " First Pass %",font = ("arial",self.fontSize))


        self.lastPartName = self.cCanvas.create_text(400+self.x,190 +self.y,text = "Last Part:      " + last[1] + "\n" + last[3],font = ("arial",self.fontSize))
        self.lastPartPercent = self.cCanvas.create_text(400+self.x,280 + self.y,text = last[2] + "%",font = ("system",int(GetSystemMetrics(0)/50)))

    def update(self,passFail,partNum,failList):
        
        if (self.count < 5):
            if (passFail == 1):
                self.totalPass += 1
            else:
                self.totalFail +=1
            self.count += 1
            self.cCanvas.itemconfig(self.firstPassLabel, text = "   Current Run" + "\nPart:      " + self.currPart + "\nCount:   " +str(self.count) + "\nUptime: " + timeElapsed(self.startTime),font = ("arial",self.fontSize))
        else:
            if (passFail == 1):
                self.totalPass += 1
            else:
                self.totalFail +=1
            self.val = round((self.totalPass / self.count) * 100, 2)
##            if (self.val < 97 and self.count > 5 and WARNING_COUNT < 2):
##                if (EMAIL_62 == 0 and self.machine == "TS2000"):
##                    WARNING_COUNT += 1
##                    EMAIL_62 = 1
##                    TSD_Email.send_email(self.machine, self.val)
##                elif (EMAIL_64 == 0 and self.machine == "TS2000 B"):
##                    WARNING_COUNT += 1
##                    EMAIL_64 = 1
##                    TSD_Email.send_email(self.machine, self.val)

            self.valArr.pop(0) 
            self.valArr.append(self.val)

            if (len(failList) > 0):
                print("test")
                
            self.cCanvas.itemconfig(self.firstPassLabel, text = "   Current Run" + "\nPart:      " + self.currPart + "\nCount:   " +str(self.count) + "\nUptime: " + timeElapsed(self.startTime),font = ("arial",self.fontSize))
            self.cCanvas.itemconfig(self.circle1, fill = getColor(self.val))
            self.cCanvas.itemconfig(self.percentDraw, text = str(self.val) + "%")
                

            self.count += 1

    def reset(self):
        self.val = 0
        self.count = 1
        self.totalPass = 0
        self.totalFail = 0
        self.startTime = time.time()


        #last = lastPart.splitlines()
        
        self.valArr = []
        for i in range(0,199):
            self.valArr.append(0)
            
        self.lineArr = [] 
        for i in range(0,199):
            self.lineArr.append(self.lCanvas.create_line(i*2+self.x,self.y,(i+1)*2+self.x,self.val+self.y,fill = 'red')) 

        self.circle1 = self.cCanvas.create_circle(155+self.x,190+self.y,150,fill = 'white')
        #self.circle2 = self.cCanvas.create_circle(400+self.x, 280+self.y,60,fill = getColor(float(last[2])))

        self.firstPassLabel = self.cCanvas.create_text(380 + self.x, 100 + self.y, text = "   Current Run" + "\nPart:      " + self.currPart + "\nCount:   " +str(self.count) + "\nUptime: " + timeElapsed(self.startTime),font = ("arial",self.fontSize))
        self.failList = Treeview(self.failFrame,height = 5)
        self.failList["columns"] = ("one","two")
        self.failList.column("#0",minwidth = 0, width = 100, stretch=NO)
        self.failList.column("one",minwidth = 0, width = 150, stretch=NO)
        self.failList.column("two",minwidth = 0, width = 250, stretch=NO)
        self.failList.heading("#0",text="Time")
        self.failList.heading("one",text="Failure")
        self.failList.heading("two",text="Solution")
        self.failList.insert("",0, text="13:30:05", values=("it not working","is it plugged in?"))
        self.failList.pack(side = LEFT)


        self.percentDraw = self.cCanvas.create_text(155+self.x,190 +self.y,text = "Initializing...",font = ("system",int(GetSystemMetrics(0)/40)))
        self.lineNameDraw = self.cCanvas.create_text(155+self.x,25 +self.y,text = self.lineName + " First Pass %",font = ("arial",self.fontSize))


        #self.lastPartName = self.cCanvas.create_text(400+self.x,190 +self.y,text = "Last Part:      " + last[1] + "\n" + last[3],font = ("arial",self.fontSize))
        #self.lastPartPercent = self.cCanvas.create_text(400+self.x,280 + self.y,text = last[2] + "%",font = ("system",int(GetSystemMetrics(0)/50)))
            
def timeElapsed(startTime):
    seconds = time.time() - startTime
    m,s = divmod(seconds,60)
    h,m = divmod(m,60)
    return str(int(h))[:3]+ ":" + str(int(m))[:2] + ":" + str(int(s))[:2]
    

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

init = graphics_init()
tsd1 = TSD_Graphics(init,"Line 62","ESP123","Line 62\nESP321\n95.9\nTues April 12 13:53:01",0,0)
tsd2 = TSD_Graphics(init,"Line 64","ESP123","Line 64\nESP321\n99.5\nTues April 12 14:22:22",500,0)

num = 0
while True:
    if randint(1,100) > 95:
        tsd1.update(2,"ESP321",[])
        tsd2.update(2,"ESP321",[])
    else:
        tsd1.update(1,"ESP321",[])
        tsd2.update(1,"ESP321",[])
    init[0].update()
    num += 1
    sleep(1)


    





    
    










