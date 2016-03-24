from graphics import *
import time

from TSD_Email import *

THRESHOLD_FAIL_PERCENTAGE = 94
THRESHOLD_WARNING_PERCENTAGE = 97
EMAIL_62 = 0
EMAIL_64 = 0
WARNING_COUNT = 0
Debug = 0

# draws two circles, one for each machine and displays current percentage in middle
class TSD_Graphics: ##x,y = bottom left corner
    def __init__(self,win,machine,lastPass,x,y):
        if (Debug == 1):
            print("Initializing")
        
        self.win = win
        win.setCoords(0,0,1000,500)
        self.machine = machine
        self.x = x
        self.y = y
        self.val = 0
        self.count = 1
        self.totalPass = 0
        self.totalFail = 0
        self.start = time.time()
        
        self.valArr = []
        for i in range(0,99): ##initialize array holding values past 100 values (queue-like structure)
            self.valArr.append(0)
            
        self.barArr = [] ##array containing rectangle objects
        for i in range(0,99):
            self.barArr.append(Rectangle(Point(i*5+self.x,self.y),Point((i+1)*25+self.x,self.val+self.y))) ##initialize array containing rectangle objects
            self.barArr[i].draw(self.win)
        
        
        self.circle = Circle(Point(250+self.x,300+self.y),190)
        self.circle.setFill('white')
        self.circle.draw(self.win)
        
        self.machine = machine
        self.machineName = Text(Point(250+self.x,375 +self.y),machine + "\nTotal Runs: "+ str(self.count) )
        self.machineName.draw(self.win)

        self.txt = Text(Point(250+self.x,295+self.y),"Initializing..." + "%")
        self.txt.setSize(36)
        self.txt.draw(self.win)

        self.lastPass = Text(Point(250+self.x,200 +self.y),"Last Pass:" + lastPass)
        self.lastPass.draw(self.win)

        self.base = Line(Point(self.x,100 + self.y),Point(1000+ self.x,100 + self.y))
        self.base.setFill('green')
        self.base.draw(self.win)

        if (Debug == 1):
            print("Finished initializing")
        

    def getName(self):
        if (Debug == 1):
            print("Get name called")
        
        return self.machine

    def getPercentage(self):
         if (Debug == 1):
            print("getPercentage called")
        
         return round((self.totalPass / self.count)* 100, 2)
    
    def update(self,passFail):
        global EMAIL_62
        global EMAIL_64
        global WARNING_COUNT

        if (Debug == 1):
            print("Update called")
        
        if (self.count < 5): ##wait for 5 pass/fail values before displaying information
            if (passFail == 1):
                self.totalPass += 1
            else:
                self.totalFail += 1
                
            self.txt.undraw()
            self.machineName.undraw()
            
            self.txt.setText("Initializing...")
            self.machineName.setText(self.machine + "\nTotal Runs: "+ str(self.count) + "\nUptime: " + str(round((time.time() - self.start)/60,0)) + " minutes")

            self.machineName.draw(self.win)
            self.txt.draw(self.win)
            self.count += 1
        else:
            if (passFail == 1):
                self.totalPass += 1
            else:
                self.totalFail += 1
            self.val = round((self.totalPass / self.count)* 100, 2)

            if (self.val < 97 and self.count > 5 and WARNING_COUNT < 2):
                if (EMAIL_62 == 0 and self.machine == "TS2000"):
                    WARNING_COUNT += 1
                    EMAIL_62 = 1
                    TSD_Email.send_email(self.machine, self.val)
                elif (EMAIL_64 == 0 and self.machine == "TS2000 B"):
                    WARNING_COUNT += 1
                    EMAIL_64 = 1
                    TSD_Email.send_email(self.machine, self.val)
                    
            
            self.valArr.pop(0) ##remove first item in list
            self.valArr.append(self.val) ##add current value to end of list
            color = getColor(self.val) 

            for i in range(0,99):
                self.barArr[i].undraw()
                self.barArr[i] = (Rectangle(Point(i*5+self.x,self.y),Point((i+1)*5+self.x,self.valArr[i]+self.y)))
                self.barArr[i].setFill(getColor(self.valArr[i]))
                self.barArr[i].draw(self.win)

            self.circle.undraw()
            self.txt.undraw()
            self.machineName.undraw()
            self.lastPass.undraw()
        
            self.circle.setFill(color)
            self.txt.setText(str(self.val)+"%")
            self.machineName.setText(self.machine + "\nTotal Runs: "+ str(self.count) + "\nUptime: " + timeHourMin((time.time() - self.start)/60))
        
            self.circle.draw(self.win)
            self.txt.draw(self.win)
            self.machineName.draw(self.win)
            self.lastPass.draw(self.win)
            self.count += 1
            
    def reset(self):
        if (Debug == 1):
            print("reset called")
        
        self.val = 0
        self.count = 1
        self.totalPass = 0
        self.start = time.time()
        
        self.valArr = []
        for i in range(0,99): 
            self.valArr.append(0)
            
        for i in range(0,99):
            self.barArr[i].undraw()
            self.barArr[i] = (Rectangle(Point(i*5,0),Point((i+1)*5,self.valArr[i])))
            self.barArr[i].setFill(getColor(self.valArr[i]))
            self.barArr[i].draw(self.win)

        self.circle.undraw()
        self.txt.undraw()
        self.machineName.undraw()

        self.circle.setFill('white')
        self.txt.setText("Initializing...")
        self.machineName.setText(self.machine + "\nTotal Runs: "+ str(self.count) + "\nUptime: " + str(round((time.time() - self.start)/60,0)) + " minutes")
    
        self.circle.draw(self.win)
        self.txt.draw(self.win)
        self.machineName.draw(self.win)

        #additional functions for graphics class
def button(cenPt, label, color, width, height, window):
    if (Debug == 1):
            print("button drawn")
        
    p1x, p1y = cenPt.getX() - width/2, cenPt.getY() - height/2
    p2x, p2y = cenPt.getX() + width/2, cenPt.getY() + height/2
    rect = Rectangle(Point(p1x,p1y), Point(p2x,p2y))
    rect.setFill(color)
    rect.draw(window)
    txt = Text(cenPt, label)
    txt.draw(window)
    return rect

def isPtInRect (pt, rect):
    if (Debug == 1):
            print("isPtInRect called")
        
    if pt != None:
        p1, p2 = rect.getP1(), rect.getP2()
        return p2.getX() >= pt.getX() >= p1.getX() and p2.getY() >= pt.getY() >= p1.getY()
    else:
        return False        

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

def timeHourMin(minutes):
    if (Debug == 1):
        print("timeHourMin called")
        
    h = str(int(minutes // 60))
    m = str(int(minutes % 60))
    return (h + " Hours, " + m + " Minutes")
