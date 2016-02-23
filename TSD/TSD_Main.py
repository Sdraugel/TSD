import TSD_Parser
import TSD_Graphics
from graphics import *

def main():
    done = False
    # intialize both TSD class and TSD_Graphics
    tsd = TSD_Parser.TSD_Parser("TS2000\n","TS2000 B\n")
    close = TSD_Graphics.button(Point(990,490),"X",'red',15,15,tsd.win)

    while (True): # need to finish function to check new .RDY file in directory
        # first part polling for mouse input, checking for reset or close button clicks
##        cPt = tsd.win.checkMouse()
##        if (isPtInRect(cPt,tsd.machine1.resetButton)):
##            tsd.machine1.reset()
##        if (isPtInRect(cPt,tsd.machine2.resetButton)):
##            tsd.machine2.reset()
##        if (isPtInRect(cPt,close)):
##            done = True

        # if new file, check rdy file matches config, then update
        if(tsd.checkNewRDY()):
            tsd.getNewRDY()
            tsd.checkMatch()
            tsd.update()
            tsd.delRDY()

       
    tsd.win.close()
main()

