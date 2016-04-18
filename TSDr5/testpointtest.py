def getTestPoints(self):
        file_path = open(self.rdyFile, 'r')
        linelist = file_path.readlines()
        for i in range(43,2551,6):
            print(linelist[i])
        
        file_path.close()
