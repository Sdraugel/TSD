
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
        total = 1
        
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

        first = 9999
        for i in range(len(linelist)):
            if  (re.search(r"E\+\d\d\n|E\-\d\d\n", linelist[i]) or str(linelist[i]) == "Not Measured!\n" or str(linelist[i]) == "passed\n" or str(linelist[i])[0] == "-"):
                count+=1
                if i < first:
                    first = i
                    print(first)

        f.close()
        
        needed = num_lines - first
        total = needed / 6
        print(total)

        if (total < total_excel):
            # Call the tkinter function to replace excelFile
            new_file_path = repace_Excel_File()
            excel_file = open(new_file_path, 'r')
            

        return

        ## This method replaces the excel document file path with a new one, using a TKinter dialogue
        def repace_Excel_File():
        	new_excel_file_path = ""

        	return new_excel_file_path

        # This method will watch the folder and pass back a new file name when created
        def folder_monitor(folderName):
        	new_file_name = ""

        	return new_file_name

        # This method will parse the .rdy file and look for the machine name and the pass # (1 or 2)
        # then pass it onto the graphics package
        def parse_pass_fail():
            machine_name = ""
            pass_result = ""

            UI(machine_name, pass_result)

        return


