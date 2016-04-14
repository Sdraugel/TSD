import os
import shutil
import xlrd
from graphics import *
from win32api import GetSystemMetrics
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import time

import TSD_Graphics
from TSD_Record import *
from TSD_Testing import *

Debug = 0
TESTING = 1
Sleep_count = 0
Sleep_timer = 3
Time_out = 3

#class that stores current RDY file as variable as well as current excel config
#also contains methods for parsing to get numbers of lines, machine name, and pass/fail values
class TSD_Parser:
    ## constructor that pulls up two subsequent file directory windows to initialize RDY and config files
    ## also instantiates one graphics window and two TSD_Graphics objects, one for each machine
    def __init__(self,machine1,machine2):

        fo = open("TSD_Record.txt", "r")
        record = fo.readlines()
        record1 = ""
        record2 = ""
        for i in range(0,4):
            record1+= record[i]
        for i in range(5,9):
            record2+= record[i]
        fo.close()
        
        self.tsd_record = TSD_Record()
        
        self.rdyFile = rdyOpen()
        self.folder = dirOpen()
        self.excelFile = excelOpen()
        self.priorityFile = excelOpen()
        self.win = GraphWin("Test Stand Diagnostics", GetSystemMetrics(0),GetSystemMetrics(0)/2)
        self.win.setBackground('white')
        self.machine1 = TSD_Graphics.TSD_Graphics(self.win,machine1,record1,0,0)
        self.machine2 = TSD_Graphics.TSD_Graphics(self.win,machine2,record2,500,0)
        self.failList = []
        if (Debug == 1):
            print("initializing parser")
        
    ## check for new file in directory
    ## return true if new file + change self.rdyFile
    ## return false if no new file
    def checkNewRDY(self):
        global Sleep_count
        global Time_out
        global Sleep_timer
        global Testing
        sourceFiles = os.listdir(self.folder)
        #print("Source Files: " + sourceFiles)

        if (Debug == 1):
            print("checkNewRdy")
            print("Sleep_count: " + str(Sleep_count))

        if (Sleep_count <Time_out):
       
            if (len(sourceFiles) > 0 and sourceFiles[len(sourceFiles)-1].endswith(".rdy")):
                #print("checking " + sourceFiles[len(sourceFiles)-1])
                Sleep_count += 0
                return True
            else:
                if (TESTING == 1):
                    Testing.populate(1)
                    Sleep_count = 0
                else:
                    Sleep_count += 1
                    time.sleep(Sleep_timer)
                    print("Sleeping......")
                    return False
        else:
            print("System timed out due to inactivity")
            sys.exit(0)

    def getNewRDY(self):
        sourceFiles = os.listdir(self.folder)
        for i in range(len(sourceFiles)):
            if (sourceFiles[i].endswith(".rdy")):
                self.rdyFile =  self.folder + "/" + sourceFiles[i]
        if (Debug == 1):
            print("getNewRDY")
        

    def delRDY(self):
        os.remove(self.rdyFile)
        if (Debug == 1):
            print("delRdy")
        

    ## check the number of tests in RDY file
    def getNumLines(self):

        file_path = open(self.rdyFile, 'r') 
        num_lines = sum(1 for line in open(self.rdyFile))
        file_path.close()

        if (Debug == 1):
            print("getNumLines")
        
        return (num_lines - 38) / 6

    ## check the number of lines in the excel config
    def getExcelRows(self):
    
        book = xlrd.open_workbook(self.excelFile)
        first_sheet = book.sheet_by_index(0)
        if (Debug == 1):
            print("getExcelRows")
        
        return first_sheet.nrows

    ## from RDY file, get the name of the machine. ex TS2000 or TS2000 B
    def getMachineName(self):

        file_path = open(self.rdyFile, 'r')
        machine_name = ""
        linelist = file_path.readlines()
        for zipplyzoops in linelist[7]:
            if zipplyzoops != '\n':
                machine_name += zipplyzoops
        if (Debug == 1):
            print("getMachineName")
        
        return machine_name


    # from the RDY file, check if overall test is 1(pass) or 2/3(fail)
    def getPassFail(self):

        file_path = open(self.rdyFile, 'r')
        linelist = file_path.readlines()
        file_path.close()
        #print("pass/fail value = " + str(linelist[19]))
        return int(linelist[19])

    def getPartNumber(self):

        file_path = open(self.rdyFile, 'r')
        partNumber = ""
        linelist = file_path.readlines()
        for zipplyzoops in linelist[4]:
            if zipplyzoops != '\n':
                partNumber += zipplyzoops
        if (Debug == 1):
            print("getPartNumber")
        
        return partNumber

    def checkTestPoints(self):
        failList = []
        count = 0
        file_path = open(self.rdyFile, 'r')
        linelist = file_path.readlines()

        book = xlrd.open_workbook(self.excelFile)
        first_sheet = book.sheet_by_index(0)
        
        for i in range(42,len(linelist),6):
            #print(first_sheet.cell(count,15).value + " " + first_sheet.cell(count,17).value +": " + linelist[i])
            count += 1
            if (int(linelist[i]) > 1):
                self.failList.append(str(first_sheet.cell(count,15).value)+ " " + str(first_sheet.cell(count,17).value) + "\n" + str(first_sheet.cell(count,18).value))
        #print ("Number of test points: " + str(count))

    
    # opens file directory window to replace current excel config
    def replaceExcel(self):
        try:
            book = xlrd.open_workbook(self.excelFile)
            first_sheet = book.sheet_by_index(0)
            #print (first_sheet.row_values(0))
        except:
            print("No File Exists")

        newFileDir = excelOpen()
        try:
            book = xlrd.open_workbook(self.excelFile)
            first_sheet = book.sheet_by_index(0)
            #print (first_sheet.row_values(0))
        except:
            print("No File Exists")

        self.excelFile = newFileDir

    # check if number of runs in RDY file matches number of excel rows
    def checkMatch(self):
        print (" ")
##        while (self.getNumLines() != self.getExcelRows()):
##            print("Number of lines in .RDY file does not match excel config" + str(self.getNumLines()))
##            self.replaceExcel()
##            self.getExcelRows()        

    #check machine name and update that machine circle in GUI class with a pass/fail value
    def update(self):
        if(self.getMachineName() == self.machine1.getName()): # check which machine name matches with the one in RDY file
            self.checkTestPoints()
            self.machine1.update(self.getPassFail(),self.getPartNumber(),self.failList)
            self.tsd_record.updateRecord1(self.getMachineName(),self.getPartNumber(),self.machine1.getPercentage())
        elif(self.getMachineName() == self.machine2.getName()):
            self.checkTestPoints()
            self.machine2.update(self.getPassFail(),self.getPartNumber(),self.failList)
            self.tsd_record.updateRecord2(self.getMachineName(),self.getPartNumber(),self.machine2.getPercentage())

        else:
            print ("Error! Machine name, " + self.getMachineName() + " does not match existing machine names!")

    def priorityCheck(self):
        prioritybook = xlrd.open_workbook(self.priorityFile)
        configbook = xlrd.open_workbook(self.excelFile)

        pb = prioritybook.sheet_by_index(0)
        priorityList = []

        for i in range(2 , pb.nrows-1 , 1):
            sub1 = pb.cell(i,0).value
            priorityList.append(sub1[3:])
            
            #priorityList.append(pb.cell(i,0).value)
            #KEEP THIS ^
        prioritySet = set(priorityList)
        
        cb = configbook.sheet_by_index(0)
        configList = []

        for i in range(1 , cb.nrows , 1):
            sub = cb.cell(i,15).value
            configList.append(sub[3:])

        configSet = set(configList)


        chooseNewPriority()
        
        #if prioritySet != configSet:
        #if set(priorityList) != set(configList):
        #    newFile = excelOpen()
        #    self.priorityFile = newFile
        #    prioritybook = xlrd.open_workbook(self.priorityFile)
        #    print("Error: Priority and Configuration files do not match.")
        
        #NEEDS WORK
        #What to do if config and priority dont match
        
def excelOpen():
    root = Tk()
    root.withdraw()
    root.update()
    filePath = askopenfilename(initialdir = "", filetypes = (("Excel Files", "*.xls"),("Excel Files","*.xlsm")),title = "Choose a new Excel File")
    root.destroy()

    return filePath


def dirOpen():
    root = Tk()
    root.withdraw()
    root.update()
    filePath = askdirectory(initialdir = "", title = "Choose the RDY folder destination")
    root.destroy()

    return filePath

def rdyOpen():
    root = Tk()
    root.withdraw()
    root.update()
    filePath = askopenfilename(initialdir = "", filetypes = (("RDY Files", "*.rdy"),("All Files","*.RDY")),title = "Choose a new RDY File")
    root.destroy()

    return filePath



            
