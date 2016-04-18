from tkinter import *
from tkinter.ttk import *
from win32api import GetSystemMetrics
import time
from time import sleep
from random import randint
from TSD_Record import *
from TSD_Email import *


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
    filemenu=Menu(menubar,tearoff = 0)
    filemenu.add_command(label="New Config File")
    filemenu.add_command(label="New Priority File")
    filemenu.add_command(label="Open Fail Log",command = openLog)
    filemenu.add_command(label="New Part")
    filemenu.add_command(label="Pause")
    filemenu.add_command(label="Exit",command = root.destroy)
    menubar.add_cascade(label = "File", menu = filemenu)

    optionmenu=Menu(menubar,tearoff = 0)
    optionmenu.add_command(label="Text Size")
    optionmenu.add_command(label="Resolution")
    optionmenu.add_command(label="DEBUG MODE")
    menubar.add_cascade(label = "Options", menu = optionmenu)

    helpmenu=Menu(menubar,tearoff = 0)
    helpmenu.add_command(label="About this program")
    helpmenu.add_command(label="Version")
    menubar.add_cascade(label = "Help", menu = helpmenu)
    
   
    root.config(menu=menubar)
    lCanvas= ResizingCanvas(root,width = GetSystemMetrics(0), height = 100, bg = 'black')
    lCanvas.pack(side =BOTTOM,expand=NO)
    frame = Frame(root,height = 50)
    frame.pack(side = BOTTOM,expand = False)
    cCanvas = ResizingCanvas(root,width = 1000, height = 500, bg = 'light grey')
    cCanvas.pack(side = LEFT,expand=YES, fill=BOTH)

    return [root,menubar,cCanvas,lCanvas,frame]
def openLog():
    os.system("notepad.exe Records\\TSD_Fail_Record.txt")

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
        for i in range(0,198):
            #self.lineArr.append(self.lCanvas.create_line(-i*2+self.x,self.y,(i+1)*-2+self.x,self.val+self.y,fill = 'red'))
            #self.lineArr.append(self.lCanvas.create_line(i+self.x,(self.valArr[i]+self.y+50),(i+1)+self.x,(self.valArr[i+1]+self.y+100),fill = 'red'))
            self.lineArr.append(self.lCanvas.create_line((i*2.5+self.x)*GetSystemMetrics(0)/1000,(self.valArr[i]*-1+100),((i+1)*2.5+self.x)*GetSystemMetrics(0)/1000,(self.valArr[i+1]*-1+100),fill = 'red'))
        
        self.circle1 = self.cCanvas.create_circle(155+self.x,190+self.y,150,fill = 'white')
        self.circle2 = self.cCanvas.create_circle(400+self.x, 280+self.y,60,fill = getColor(float(last[2])))

        self.firstPassLabel = self.cCanvas.create_text(380 + self.x,
                                                       100 + self.y,
                                                       text = "   Current Run" + "\nPart:      " +
                                                       self.currPart + "\nCount:   " +str(self.count) +
                                                       "\nUptime: " + timeElapsed(self.startTime),
                                                       font = ("arial",self.fontSize))
        self.failList = Treeview(self.failFrame,height = 5)
        self.failList["columns"] = ("one","two")
        self.failList.column("#0",minwidth = 0, width = int(GetSystemMetrics(0)/10), stretch=NO)
        self.failList.column("one",minwidth = 0, width = int(GetSystemMetrics(0)/5), stretch=NO)
        self.failList.column("two",minwidth = 0, width = int(GetSystemMetrics(0)/5), stretch=NO)
        self.failList.heading("#0",text="Time")
        self.failList.heading("one",text="Failure")
        self.failList.heading("two",text="Recommended Fix")
        self.failList.insert("",0, text="13:30:05", values=("it not working","is it plugged in?"))
        self.failList.pack(side = LEFT)

        print("Line Name: " + self.lineName)

        self.percentDraw = self.cCanvas.create_text(155+self.x,190 +self.y,text = "Initializing...",font = ("system",int(GetSystemMetrics(0)/30)))
        self.lineNameDraw = self.cCanvas.create_text(155+self.x,25 +self.y,text = self.lineName + " First Pass %",font = ("arial",self.fontSize))


        self.lastPartName = self.cCanvas.create_text(400+self.x,190 +self.y,text = "Last Part:      " + last[1] + "\n" + last[3],font = ("arial",self.fontSize),fill = "#404040")
        self.lastPartPercent = self.cCanvas.create_text(400+self.x,280 + self.y,text = last[2] + "%",font = ("system",int(GetSystemMetrics(0)/50)))

    def update(self,passFail,partNum,failName):
        global EMAIL_62
        global EMAIL_64
        global WARNING_COUNT
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
            if (self.val < 97 and self.count > 5 and WARNING_COUNT < 2):
                if (EMAIL_62 == 0 and self.lineName == "62"):
                    WARNING_COUNT += 1
                    EMAIL_62 = 1
                    TSD_Email.send_email(self.lineName, self.val)
                elif (EMAIL_64 == 0 and self.lineName == "64"):
                    WARNING_COUNT += 1
                    EMAIL_64 = 1
                    TSD_Email.send_email(self.lineName, self.val)

            self.valArr.pop(0) 
            self.valArr.append(self.val)
            for i in range(0,198):
                self.lCanvas.coords(self.lineArr[i],((i*2.5+self.x)*GetSystemMetrics(0)/1000,(self.valArr[i]*-4+410),((i+1)*2.5+self.x)*GetSystemMetrics(0)/1000,(self.valArr[i+1]*-4+410)))
        

            

            if (failName != None):
                self.failList.insert("",0,text = time.asctime( time.localtime(time.time()) ), values = (getFailure(failName),getFix(failName)))
                fo = open("Records\\TSD_Fail_Record.txt", "a")
                fo.write("%s %s %s %s %s\n" % (time.asctime( time.localtime(time.time())),self.lineName,self.currPart,getFailure(failName),getFix(failName)))
                fo.close()
                                     
                
            self.cCanvas.itemconfig(self.firstPassLabel, text = "   Current Run" + "\nPart:      " + self.currPart + "\nCount:   " +str(self.count) + "\nUptime: " + timeElapsed(self.startTime),font = ("arial",self.fontSize))
            self.cCanvas.itemconfig(self.circle1, fill = getColor(self.val))
            self.cCanvas.itemconfig(self.percentDraw, text = str(self.val) + "%")
                

            self.count += 1

    
    #def reset(self):

    def getName(self):
        if (Debug == 1):
            print("Get name called")
        
        return self.lineName

    def getPercentage(self):
         if (Debug == 1):
            print("getPercentage called")
        
         return round((self.totalPass / self.count)* 100, 2)

        
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

def getFix(failure): ##placeholder function
    returned_value = ""
    for char in failure:
        if char == ",":
            returned_value = ""
        else:
            returned_value += char
    if returned_value == "":
        returned_value = "No fix data"
    return returned_value

def getFailure(failure):
    returned_value = ""
    for char in failure:
        if char == ",":
            break
        else:
            returned_value += char
    return returned_value

##init = graphics_init()
##tsd1 = TSD_Graphics(init,"Line 62","ESP123","Line 62\nESP321\n95.9\nTues April 12 13:53:01",0,0)
##tsd2 = TSD_Graphics(init,"Line 64","ESP123","Line 64\nESP321\n99.5\nTues April 12 14:22:22",500,0)
##
##num = 0
##while True:
##    if randint(1,100) > 95:
##        tsd1.update(2,"ESP321","it not running")
##        tsd2.update(2,"ESP321","it not running")
##    else:
##        tsd1.update(1,"ESP321","")
##        tsd2.update(1,"ESP321","")
##    init[0].update()
##    num += 1
##    sleep(.1)


    





    
    










