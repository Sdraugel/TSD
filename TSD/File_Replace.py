from tkinter import *
from tkinter.filedialog import askopenfilename
import xlrd

def fileOpen():
    root = Tk()
    root.withdraw()
    root.update()
    filePath = askopenfilename(initialdir = "", filetypes = (("Excel Files", "*.xls"),("Excel Files","*.xlsm")),title = "Choose a new Excel File")
    root.destroy()

    return filePath

def replaceFile(excelDoc):
    try:
        book = xlrd.open_workbook(excelDoc)
        first_sheet = book.sheet_by_index(0)
        print (first_sheet.row_values(0))
    except:
        print("No File Exists")

    newFileDir = fileOpen()
    try:
        book = xlrd.open_workbook(excelDoc)
        first_sheet = book.sheet_by_index(0)
        print (first_sheet.row_values(0))
    except:
        print("No File Exists")

    return newFileDir
        


