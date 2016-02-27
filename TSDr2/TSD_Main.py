from graphics import *

from TSD_Testing import *
from TSD_Parser import *
from TSD_Graphics import *

class Main(object):
		
        def main():
                # intialize both TSD class and TSD_Graphics
                #tsd = TSD_Parser.TSD_Parser("TS2000","TS2000 B")
                #close = TSD_Graphics.button(Point(990,490),"X",'red',15,15,tsd.win)

                DEBUG = True

                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # Monitors the test_results folder for new files
                #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                # pc
                #dir_loc = os.path.dirname(os.path.abspath(__file__)) + '\\test_results'

                # mac
                dir_loc = os.path.dirname(os.path.abspath(__file__)) + '/test_results'
                excelFile = os.path.dirname(os.path.abspath(__file__)) + '/config.xls'
                sleep_count = 0
                time_out = 3
                sleep_time = 3
                start = True

                win = GraphWin("Test Stand Diagnostics", 1200,600)
                machine1 = TSD_Graphics(win,"TS2000",0,0)
                machine2 = TSD_Graphics(win,"TS2000B",500,0)

                TSD_Testing.populate(3)

                while (sleep_count < time_out):
                        print(os.listdir(dir_loc)) 
                        if os.listdir(dir_loc) == [".DS_Store"]:
                                sleep_count += 1
                                print("sleeping..." + "\n")
                                time.sleep(sleep_time)
                        else:
                                for filename in os.listdir(dir_loc):
                                        if filename.endswith(".rdy"):
                                                file_path = dir_loc + "/" + filename
                                                numLinesRDY = TSD_Parser.getNumLines(file_path)
                                                numLinesExcel = TSD_Parser.getExcelRows(excelFile)
                                                machine_name = TSD_Parser.getMachineName(file_path)
                                                pass_fail = TSD_Parser.getPassFail(file_path)
                                                if (DEBUG == True):
                                                        print("Machine Name: " + machine_name)
                                                        print("Excel Lines: " + str(numLinesExcel))
                                                        print("RDY Lines: " + str(numLinesRDY))
                                                        print("Pass: " + str(pass_fail))
                                                        TSD_Graphics.update(machine_name, pass_fail)                                                      

                                                #pc
                                                #os.remove(dir_loc + '\\' + filename)

                                                #mac
                                                os.remove(dir_loc + '/' + filename)

                                                time.sleep(sleep_time)
                if (sleep_count == time_out):
                    print("Exiting due to inactivity")
                            
                return

       
#        tsd.win.close()
Main.main()

