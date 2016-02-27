import os
import shutil
import xlrd
from graphics import *
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import askdirectory
import random


class TSD_Testing():
        """docstring for Testing"""
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Populates the test_results folder with fake data for testing purposes
        #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        def populate(N):
                print("Populating result_files folder")
                file_list = []
                destination = os.path.dirname(os.path.abspath(__file__)) + '/test_results'
                #pc
                #dir_loc = os.path.dirname(os.path.abspath(__file__)) + '\\master_files'

                #mac
                dir_loc = os.path.dirname(os.path.abspath(__file__)) + '/master_files'

                for file in os.listdir(dir_loc):

                        # pc
                        #file_list.append(dir_loc + '\\' + file)

                        #mac
                        file_list.append(dir_loc + '/' + file)

                total_files = len(file_list)
                for i in range(N):
                        selection = random.randrange(total_files)
                        shutil.copy(file_list[selection], destination)
                           
                print("Files successfully moved")
                return

		
