import os
import sys
import random

if __name__ == '__main__':
    name = './vm_snapshots/'
    files = [name+'sim_0_3_512_256.dat', name+'sim_1_5_1024_256.dat', name+'sim_2_5_1024_512.dat', name+'sim_3_5_1024_768.dat', name+'sim_4_10_1024_256.dat', name+'sim_5_10_1024_512.dat']

    

    print("0: sim_0_3_512_256.dat")
    print('1: sim_1_5_1024_256.dat')
    print("2: sim_2_5_1024_512.dat")
    print("3: sim_3_5_1024_768.dat")
    print("4: sim_4_10_1024_256.dat")
    print("5: sim_5_10_1024_512.dat")
    choice = input("Which file would you like to use? (Input 0-5): ")

    p = files[int(choice)]            # path to file
    f = os.path.basename(p)                             # get basename (remove path)
    name, ext = f.split('.')                            # split name from extension
    s,run,np,vm,pm = name.split('_')  # get each piece of info

    inputFile = open(p, 'r')

    pmTable = {}

    for x in range(int(pm)):
        #[0] = name, [1] = access count, [2] = last access
        pmTable[str(x)] = ['', 0, 1]

    inputFile = inputFile.read()
    inputFile = inputFile.split(' ')
    inputFile.pop(len(inputFile) - 1)

    print("0: FIFO")
    print("1: Least Recently Used")
    print("2: Least Frequently Used")
    print("3: Random Replacement")
    token = input("What algorithm would you like to use?: ")
        
    page_fault = 0

    if token == '0':
        FIFO = 0
        for line in inputFile:
            process, location = line.split(',')
            location = location.strip('0x')
            
            found = False 

            for k in pmTable:
                if pmTable[k][0] == location:
                    found = True

            if not found:
                pmTable[str(FIFO)][0] = location
                print(line + ' = ' + 'Process ' + process + ' accesses line ' + str(FIFO))
                page_fault += 1
                if FIFO < int(pm) - 1:
                    FIFO += 1
                else:
                    FIFO = 0
        print(page_fault)

    if token == '1':
        initialize = -1
        time = 0

        for line in inputFile:
            process, location = line.split(',')
            location = location.strip('0x')
            
            found = False
            for k in pmTable:
                if pmTable[k][0] == location:
                    found = True

            if not found:
                initialize += 1

            found = False
            
            for k in pmTable:
                if pmTable[k][0] == location and not found:
                    pmTable[k][2] = time
                    found = True
                elif int(k) == int(pm) - 1 and not found and initialize >= int(pm):
                    leastUsedNum = sys.maxsize
                    leastUsedK = ''
                    for key in pmTable:
                        if pmTable[key][2] < leastUsedNum:
                            leastUsedNum = pmTable[key][2]
                            leastUsedK = key
                    print(line + ' = ' + 'Process ' + process + ' accesses line ' + leastUsedK)
                    page_fault += 1
                    pmTable[leastUsedK][0] = location
                    pmTable[leastUsedK][2] = time
                    found = True
                elif initialize < int(pm) and not found:
                    pmTable[str(initialize)][0] = location
                    pmTable[str(initialize)][2] = time
                    print(line + ' = ' + 'Process ' + process + ' accesses line ' + str(initialize))
                    page_fault += 1
                    found = True
            time += 1
        print(page_fault)
            

    if token == '2':
        initialize = -1
        time = 0

        for line in inputFile:
            process, location = line.split(',')
            location = location.strip('0x')
            

            found = False
            for k in pmTable:
                if pmTable[k][0] == location:
                    found = True

            if not found:
                initialize += 1

            found = False
            
            for k in pmTable:
                if pmTable[k][0] == location and not found:
                    pmTable[k][1] += 1
                    pmTable[k][2] = time
                    found = True
                elif int(k) == int(pm) - 1 and not found and initialize >= int(pm):
                    leastUsedNum = sys.maxsize
                    leastUsedK = ''
                    for key in pmTable:
                        if pmTable[key][1]/time < leastUsedNum:
                            leastUsedNum = pmTable[key][2]
                            leastUsedK = key
                    print(line + ' = ' + 'Process ' + process + ' accesses line ' + leastUsedK)
                    page_fault += 1
                    pmTable[leastUsedK][0] = location
                    pmTable[leastUsedK][2] = time
                    found = True
                elif initialize < int(pm) and not found:
                    pmTable[str(initialize)][0] = location
                    pmTable[str(initialize)][2] = time
                    print(line + ' = ' + 'Process ' + process + ' accesses line ' + str(initialize))
                    page_fault += 1
                    found = True
            time += 1

        print(page_fault)

            
    if token == '3':
        initialize = 0
        for line in inputFile:
            process, location = line.split(',')
            location = location.strip('0x')

            if initialize < int(pm):
                pmTable[str(initialize)][0] = location
                print(line + ' = ' + 'Process ' + process + ' accesses line ' + str(initialize))
                page_fault += 1
                initialize += 1
            else:
                found = False
                for k in pmTable:
                    if pmTable[k][0] == location:
                        found = True
                    elif int(k) == int(pm) - 1 and not found:
                        r = random.randint(0, int(pm) - 1)
                        print(line + ' = ' + 'Process ' + process + ' accesses line ' + str(r))
                        page_fault += 1
                        pmTable[str(r)][0] = location
        print(page_fault)


                












