## Parses through the machine datafile
## Returns the total number of tests run

import re
import sys

class TSD:
    def parser(folderName, fileName, excelFile):


        start = 0
        count = 0
        total = 1
        total_excel = 0 # The excel document's number of lines

        folderName = folderName # folder containing .RDY files
        fileName = folderName + '/' + fileName # .RDY file name
        f = open(filaName, 'r')

        e = open(excelFile, 'r')
        total_excel = len(e.readlines())
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
            replaceExcelFile(folderName, fileName)
            
            
        # Call the % output part of the program           
        return tally(folderName, fileName, excelFile) 
        

    parser()


