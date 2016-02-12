import Parsers
import TSD_Graphics

class TSD:

    def main():
    	done = 0
    	wait_count = 0

    	# Predifined folder location
    	folderName = ""

    	# Predifined .rdy file name, eventually this will call a method in the parser program that monitors
    	# the contents of the folderName
    	fileName = ""

    	# Predifined .rdy file name
    	excelFile = ""

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
