## Parses through the machine datafile
## Returns the total number of tests run

import re
import sys

def parser():


    start = 0
    count = 0
    total = 1

    f = open('bh5nd64t56A2127B.txt', 'r')
    num_lines = sum(1 for line in open('bh5nd64t56A2127B.txt'))

    linelist = f.readlines()

    first = 9999
    for i in range(len(linelist)):
        if  (re.search(r"E\+\d\d\n|E\-\d\d\n", linelist[i]) or str(linelist[i]) == "Not Measured!\n" or str(linelist[i]) == "passed\n" or str(linelist[i])[0] == "-"):
            count+=1
            if i < first:
                first = i
                print(first)

    f.close()
    
    needed = num_lines - first
    total = needed / 6
    print(total)
    return total    
    
  


parser()


