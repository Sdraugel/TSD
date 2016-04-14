import time

class TSD_Record:

    def __init__(self,machine1Name = None,partNumber1=None,percentage1=0,time1=None,machine2Name = None,partNumber2=None,percentage2=0,time2=None):
        self.machine1Name = str(machine1Name)
        self.partNumber1 = str(partNumber1)
        self.percentage1 = str(percentage1)
        self.time1 = str(time1)
        self.machine2Name = str(machine2Name)
        self.partNumber2 = str(partNumber2)
        self.percentage2 = str(percentage2)
        self.time2 = str(time2)

        fo1 = open("Records\\TSD_Record1.txt", "w+")
        fo1.write("%s\n%s\n%s\n%s\n" % (self.machine1Name,self.partNumber1,self.percentage1,self.time1))
        fo1.close()

        fo2 = open("Records\\TSD_Record2.txt", "w+")
        fo2.write("%s\n%s\n%s\n%s\n" % (self.machine2Name,self.partNumber2,self.percentage2,self.time2))
        fo2.close()
      


    def updateRecord1(self,machine1Name,partNumber1,percentage1):
        self.machine1Name = str(machine1Name)
        self.partNumber1 = str(partNumber1)
        self.percentage1 = str(percentage1)
        self.time1 = str(time.asctime( time.localtime(time.time()) ))

        fo = open("Records\\TSD_Record1.txt", "w+")
        fo.write("%s\n%s\n%s\n%s\n" % (self.machine1Name,self.partNumber1,self.percentage1,self.time1))
        fo.close()

    def updateRecord2(self,machine2Name,partNumber2,percentage2):
        self.machine2Name = str(machine2Name)
        self.partNumber2 = str(partNumber2)
        self.percentage2 = str(percentage2)
        self.time2 = str(time.asctime( time.localtime(time.time()) ))

        fo = open("Records\\TSD_Record2.txt", "w+")
        fo.write("%s\n%s\n%s\n%s\n" % (self.machine2Name,self.partNumber2,self.percentage2,self.time2))
        fo.close()

        

    
