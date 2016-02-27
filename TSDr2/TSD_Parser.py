import os
import shutil
import xlrd
from graphics import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory

import TSD_Graphics


DEBUG = 1

#class that stores current RDY file as variable as well as current excel config
#also contains methods for parsing to get numbers of lines, machine name, and pass/fail values
class TSD_Parser:

    ## check the number of tests in RDY file
    def getNumLines(fileName):
        file_path = open(fileName, "r") 
        num_lines = sum(1 for line in open(fileName))
        file_path.close()
        return (num_lines - 38) / 6

    ## check the number of lines in the excel config
    def getExcelRows(fileName):
        book = xlrd.open_workbook(fileName)
        first_sheet = book.sheet_by_index(0)
        return first_sheet.nrows

    ## from RDY file, get the name of the machine. ex TS2000 or TS2000 B
    def getMachineName(fileName):

        file_path = open(fileName, 'r')
        machine_name = ""
        linelist = file_path.readlines()
        for line in linelist[7]:
            if line != '\n':
                machine_name += line

        file_path.close()
        return machine_name

    # from the RDY file, check if overall test is 1(pass) or 2/3(fail)
    def getPassFail(fileName):

        file_path = open(fileName, 'r')
        linelist = file_path.readlines()
        file_path.close()
        return int(linelist[19])



            
