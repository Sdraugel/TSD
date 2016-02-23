
# This class houses the parsers that collect data from the 
# .rdy file and pass them along to the graphics class
import re
import sys

class Parsers:

	## Parses through the machine datafile
	## Returns the total number of tests run
    def parser(folderName, fileName, excelFile):
        start = 0
        count = 0
        
        # The excel document's number of lines
        total_excel = 0 

        # folder containing .RDY files
        folderName = folderName 
        
        # .RDY file name added to the file path
        fileName = folderName + '/' + fileName 
        
        # open the .rdy file for reading
        file_path = open(fileName, 'r') 

        # open the excel file for reading
        excel_file = open(excelFile, 'r') 
        
        # length of excel file
        total_excel = len(excel_file.readlines()) 
        num_lines = sum(1 for line in open(fileName))
        linelist = f.readlines()



        pass_fail = linelist[19]
        machine_name = linelist[7]

        ##parse_pass_fail(pass_fail, machine_name)


        
        f.close()
        
         
        total = (num_lines - 38) / 6
    

        if (total != total_excel):
            # Call the tkinter function to replace excelFile
            new_file_path = repaceFile(excel_file)
            excel_file = open(new_file_path, 'r')
            

        return pass_fail, machine_name



        def fileOpen():
            root = Tk()
            root.withdraw()
            root.update()
            filePath = askopenfilename(initialdir = "", filetypes = (("Excel Files", "*.xls"),("Excel Files","*.xlsm")),title = "Choose a new Excel File")
            root.destroy()

            return filePath
        
        # This method replaces the excel document file path with a new one, using a TKinter dialogue
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

        # This method will watch the folder and pass back a new file name when created
        def folder_monitor(folderName):
        	new_file_name = ""

        	return new_file_name

        # This method will parse the .rdy file and look for the machine name and the pass # (1 or 2)
        # then pass it onto the graphics package
        def parse_pass_fail(passOrFail, machine):
            
            
            machine_name = machine
            pass_result = passOrFail

            UI(machine_name, pass_result)

        return





