from graphics import *
from time import sleep
import random
import time

def passed (i): ##function that increases failures as count increases
    rand = random.randint(0,i)
    return rand < 20

def button(cenPt, label, color, width, height, window):
    p1x, p1y = cenPt.getX() - width/2, cenPt.getY() - height/2
    p2x, p2y = cenPt.getX() + width/2, cenPt.getY() + height/2
    rect = Rectangle(Point(p1x,p1y), Point(p2x,p2y))
    rect.setFill(color)
    rect.draw(window)
    txt = Text(cenPt, label)
    txt.draw(window)
    return rect

def isPtInRect (pt, rect):
    if pt != None:
        p1, p2 = rect.getP1(), rect.getP2()
        return p2.getX() >= pt.getX() >= p1.getX() and p2.getY() >= pt.getY() >= p1.getY()
    else:
        return False        

class tsd: ##x,y = bottom left corner
    def __init__(self,win,machine,x,y):
        self.win = win
        win.setCoords(0,0,1000,500)
        self.machine = machine
        self.x = x
        self.y = y
        self.val = 0
        self.count = 1
        self.totalPass = 0
        self.start = time.time()
        
        self.valArr = []
        for i in range(0,99): ##initialize array holding values past 100 values (queue-like structure)
            self.valArr.append(0)
            
        self.barArr = [] ##array containing rectangle objects
        for i in range(0,99):
            self.barArr.append(Rectangle(Point(i*5+self.x,self.y),Point((i+1)*25+self.x,self.val+self.y))) ##initialize array containing rectangle objects
            self.barArr[i].draw(self.win)

        self.txt = Text(Point(250+self.x,295+self.y),str(self.val) + "%")
        self.txt.setSize(36)
        self.txt.draw(self.win)

        self.machine = machine
        self.machineName = Text(Point(50+self.x,475 +self.y),machine + "\nTotal Runs: "+ str(self.count) )
        self.machineName.draw(self.win)

        self.circle = Circle(Point(250+self.x,300+self.y),190)
        self.circle.setFill('white')
        self.circle.draw(self.win)

        self.base = Line(Point(self.x,100 + self.y),Point(1000+ self.x,100 + self.y))
        self.base.setFill('green')
        self.base.draw(self.win)

        self.resetButton = button(Point(50+self.x,140+self.y),"reset",'gray',50,20,win)

    
    def update(self,passed):

        if (passed):
            self.totalPass += 1
        self.val = round((self.totalPass / self.count) * 100, 2)
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
    
        self.circle.setFill(color)
        self.txt.setText(str(self.val)+"%")
        self.machineName.setText(self.machine + "\nTotal Runs: "+ str(self.count) + "\nUptime: " + str(round((time.time() - self.start)/60,0)) + " minutes")
    
        self.circle.draw(self.win)
        self.txt.draw(self.win)
        self.machineName.draw(self.win)
        self.count += 1

    def reset(self):
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

        self.circle.setFill('white')
        self.txt.setText(str(self.val)+"%")
    
        self.circle.draw(self.win)
        self.txt.draw(self.win)

def getColor(var):
    if var < 70:
        color = 'red'
    elif var < 80:
        color = 'sienna1'
    elif var < 90:
        color = 'yellow3'
    else:
        color = 'SeaGreen3'
    return color

def main():

    win = GraphWin("Test Stand Diagnostics", 1200,600)
    machine1 = tsd(win,"machine1",0,0)
    machine2 = tsd(win,"machine2",500,0)
    close = button(Point(990,490),"X",'red',15,15,win)
    i=0
    while(True):
        machine1.update(passed(i))
        machine2.update(passed(i))
        cPt = win.checkMouse()
        if (isPtInRect(cPt,machine1.resetButton)):
            machine1.reset()
        if (isPtInRect(cPt,machine2.resetButton)):
            machine2.reset()
        if (isPtInRect(cPt,close)):
            break
        i += 1
    win.close()
        
main()
