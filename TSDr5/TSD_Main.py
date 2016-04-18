import TSD_Parser
import TSD_Graphics
from graphics import *

def main():
    done = False
    # intialize both TSD class and TSD_Graphics
    tsd = TSD_Parser.TSD_Parser("TS2000","TS2000 B")

    while (True): 
        if(tsd.checkNewRDY()):
            tsd.getNewRDY()
            #tsd.checkMatch()
            tsd.update()
            tsd.delRDY()


       

main()

