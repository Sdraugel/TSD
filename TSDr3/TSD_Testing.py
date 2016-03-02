#!/usr/bin/env python
#PROG Steven Draugel
#PROJ TSD
#DATE

# Import bank
import importlib
import sys
from os.path import *
import os
import sys
import getopt
import shutil
import time
import random

DEBUG = 0

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Handles all of the file IO for the TSD program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Testing:

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Populates the test_results folder with fake data for testing purposes
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def populate(N):

        if (DEBUG == 1):
            print("Populating result_files folder with " + str(N) + " files.")
        else:
            file_list = []
            dir_loc = os.path.dirname(os.path.abspath(__file__)) + '\\source'
            source = os.path.dirname(os.path.abspath(__file__)) + '\\testing_files'
        for file in os.listdir(source):
            file_list.append(source + '\\' + file)
        
        total_files = len(file_list)
        for i in range(N):
            selection = random.randrange(total_files)
            shutil.copy(file_list[selection], dir_loc)
                   
        print("Files successfully moved")
        return
