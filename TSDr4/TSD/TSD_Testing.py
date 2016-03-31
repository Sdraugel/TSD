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

DEBUG = 1

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Handles all of the file IO for the TSD program
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
class Testing:

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    # Populates the test_results folder with fake data for testing purposes
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def populate(N):
        source = ""
        dir_loc = ""

        if (DEBUG == 1):
            print("Populating result_files folder with " + str(N) + " files.")

        file_list = []
        dir_loc = os.path.dirname(os.path.abspath(__file__)) + '\\source'
        source = '//bh5ac01s/sw_mgt/TEF1Ctrl/TEF1Exchange/ChP Payne/TD files'
        ##source = '\\Users\\isy1ch\\Desktop\\TD_Files_Backup'

        for file in os.listdir(source):
            file_list.append(source + '\\' + file)
        
        total_files = len(file_list)
        for i in range(N):
            ##selection = random.randrange(total_files)
            print("File: " + file_list[i])
            shutil.copy(file_list[i], dir_loc)
            os.remove(file_list[i])

        time.sleep(2)           
        print("Files moved from " + source + "to " + dir_loc)
        return
