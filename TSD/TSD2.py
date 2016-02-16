import re
import sys
from graphics import *
from time import *
from tkinter import *
from tkinter.filedialog import askopenfilename
import xlrd

#class that stores current RDY file as variable as well as current excel config
#also contains methods for parsing to get numbers of lines, machine name, and pass/fail values
class TSD:
    ## constructor that pulls up two subsequent file directory windows to initialize RDY and config files
    ## also instantiates one graphics window and two TSD_Graphics objects, one for each machine
    def __init__(self,machine1,machine2):
        self.rdyFile = rdyOpen()
        self.excelFile = excelOpen()
        self.win =GraphWin("Test Stand Diagnostics", 1200,600)
        self.machine1 = TSD_Graphics(win,machine1,0,0)
        self.machine2 = TSD_Graphics(win,machine2,500,0)

    def checkNewRDY(self):
        ## check for new file in directory
        ## return true if new file + change self.rdyFile
        ## return false if no new file

    ## check the number of tests in RDY file
    def getNumLines(self):

        file_path = open(self.rdyFile 'r') 
        num_lines = sum(1 for line in open(self.rdyFile))
        file_path.close()
        return (num_lines - 38) / 6

    ## check the number of lines in the excel config
    def getExcelRows(excelFile):
    
        book = xlrd.open_workbook(self.excelFile)
        first_sheet = book.sheet_by_index(0)
        return first_sheet.nrows

    ## from RDY file, get the name of the machine. ex TS2000 or TS2000 B
    def getMachineName(self):

        file_path = open(self.rdyFile 'r') 
        linelist = file_path.readlines()
        file_path.close()
        return linelist[7]

    # from the RDY file, check if overall test is 1(pass) or 2/3(fail)
    def getPassFail(self):

        file_path = open(self.rdyFile 'r')
        linelist = file_path.readlines()
        file_path.close()
        return linelist[19]
    
    # opens file directory window to replace current excel config
    def replaceExcel(self):
        try:
            book = xlrd.open_workbook(self.excelFile)
            first_sheet = book.sheet_by_index(0)
            print (first_sheet.row_values(0))
        except:
            print("No File Exists")

        newFileDir = ExcelOpen()
        try:
            book = xlrd.open_workbook(self.excelFile)
            first_sheet = book.sheet_by_index(0)
            print (first_sheet.row_values(0))
        except:
            print("No File Exists")

        self.excelFile = newFileDir

    # check if number of runs in RDY file matches number of excel rows
    def checkMatch(self):
        while (self.getNumLines() != self.getExcelRows()):
            print("Number of lines in .RDY file does not match excel config")
            replaceExcel()
            getExcelRows()        

    #check machine name and update that machine circle in GUI class with a pass/fail value
    def update(self):
        if(self.getMachineName() == self.machine1.getName()): # check which machine name matches with the one in RDY file
            self.machine1.update(self.getPassFail)
        else if(self.getMachineName() == self.machine2.getName()):
            self.machine2.update(self.getPassFail)
        else:
            print ("Error! Machine name, " + self.getMachineName() + " does not match existing machine names!")
        #TODO:delete current RDY file

# draws two circles, one for each machine and displays current percentage in middle
class TSD_Graphics: ##x,y = bottom left corner
    def __init__(self,win,machine,x,y):
        self.win = win
        win.setCoords(0,0,1000,500)
        self.machine = machine
        self.x = x
        self.y = y
        self.val = 0
        self.count = 1
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

    def getName(self):
        return self.machine
    
    def update(self,percentage):
        self.val = round(percentage * 100, 2)
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
# additional functions for graphics class
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

# file open functions using tkinter
def excelOpen():
    root = Tk()
    root.withdraw()
    root.update()
    filePath = askopenfilename(initialdir = "", filetypes = (("Excel Files", "*.xls"),("Excel Files","*.xlsm")),title = "Choose a new Excel File")
    root.destroy()

    return filePath

def rdyOpen():
    root = Tk()
    root.withdraw()
    root.update()
    filePath = askopenfilename(initialdir = "", filetypes = (("RDY Files", "*.RDY")),title = "Choose a new RDY File")
    root.destroy()

    return filePath

def main():
    done = False
    # intialize both TSD class and TSD_Graphics
    tsd = TSD("TS2000","TS2000 B")

    while (!done): # need to finish function to check new .RDY file in directory
        # first part polling for mouse input, checking for reset or close button clicks
        cPt = win.checkMouse()
        if (isPtInRect(cPt,tsd.machine1.resetButton)):
            machine1.reset()
        if (isPtInRect(cPt,tsd.machine2.resetButton)):
            machine2.reset()
        if (isPtInRect(cPt,close)):
            done = True

        # if new file, check rdy file matches config, then update
        if(tsd.checknewRDY):
            tsd.checkMatch()
            tsd.update()
            
    tsd.win.close()
