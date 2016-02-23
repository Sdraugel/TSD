import shutil
from time import sleep
import random
import os
from tkinter import *


def getRDY():
    print ("The dir is: %s" %os.listdir("source/"))
    sourceFiles = os.listdir("source/")
    while (True):
        rand = random.randint(1,len(sourceFiles)-1)
        source = "source/" + sourceFiles[rand]
        print("adding " + source)
        shutil.copy(source,"dest/")
        dest = "dest/" + sourceFiles[rand]
        sleep(3)

    
getRDY()



