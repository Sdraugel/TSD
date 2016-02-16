import Parsers
import TSD_Graphics
import tsd_GUI.py

class TSD:

    def main():
        done = 0
        wait_count = 0

        # Predifined folder location
        folderName = r'C:\Users\aaron.monahan\Documents\GitHub\CSCI462'

        # Predifined .rdy file name, eventually this will call a method in the parser program
        # that monitors the contents of the folderName
        fileName = r"\bh5nd64t56A2127B.RDY"

        # Predifined .xlsx file name
        excelFile = r"\20160122154835.xlsx"

        #fileName = fileOpen()
        
        
        while(done != 1):

            if (wait_count > 5):
                done = 1
            else :
                fileName = folder_monitor(folderName)

                if (fileName != ""):
                    parser(folderName, fileName, excelFile)
                    
                else:
                    wait()
                    wait_count += 1

        
        
        return


     # Method that keeps track of the time, when 17 seconds has passed then return
    def wait():

        return

    main()
