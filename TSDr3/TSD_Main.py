import TSD_Parser
import TSD_Graphics
from graphics import *

def main():
    done = False
    # intialize both TSD class and TSD_Graphics
    tsd = TSD_Parser.TSD_Parser("TS2000","TS2000 B")

    while (not done): # need to finish function to check new .RDY file in directory
        # first part polling for mouse input, checking for reset or close button clicks


        # if new file, check rdy file matches config, then update
        if(tsd.checkNewRDY()):
            tsd.getNewRDY()
            tsd.checkMatch()
            tsd.update()
            tsd.delRDY()
    main()

       

main()

