import os
import sys
import random

if __name__ == '__main__':
    name = './vm_snapshots/'
    files = [name+'sim_0_3_512_256.dat', name+'sim_1_5_1024_256.dat', name+'sim_2_5_1024_512.dat', name+'sim_3_5_1024_768.dat', name+'sim_4_10_1024_256.dat', name+'sim_5_10_1024_512.dat']

    #PCB[0] = name, PCB[1] = last access, PCB[2] = access count
    memoryInfo = ['',0, 0]

    '''print("0: sim_0_3_512_256.dat")
    print('1: sim_1_5_1024_256.dat')
    print("2: sim_2_5_1024_512.dat")
    print("3: sim_3_5_1024_768.dat")
    print("4: sim_4_10_1024_256.dat")
    print("5: sim_5_10_1024_512.dat")
    choice = input("Which file would you like to use? (Input 0-5): ")'''

    #p = files[int(choice)]            # path to file
    p = name+'sim_6_3_16_4.dat'
    f = os.path.basename(p)                             # get basename (remove path)
    name, ext = f.split('.')                            # split name from extension
    s,run,np,vm,pm = name.split('_')  # get each piece of info

    inputFile = open(p, 'r')

    pmTable = {}

    for x in range(int(pm)):
        pmTable[str(x)] = memoryInfo

    inputFile = inputFile.read()
    inputFile = inputFile.split(' ')

    print("0: FIFO")
    print("1: Least Recently Used")
    print("2: Least Frequently Used")
    print("3: Random Replacement")
    print("4: Optimal Replacement")
    token = input("What algorithm would you like to use?: ")

    if token == '0':
        FIFO = 0
    elif token == '3':
        r = random.randint(0, int(vm) - 1)

    page_fault = 0

    if token == '0':
        for line in inputFile:
                process, location = line.split(',')
                location = location.strip('0x')

                found = False

                for k in pmTable:
                    if pmTable[k][0] == location:
                        found = True
                    elif int(k) == int(pm) - 1 and not found:
                        pmTable[str(FIFO)][0] = location
                        print(line + ' = ' + 'Process ' + process + ' accesses line ' + str(FIFO))
                        page_fault += 1
                        if FIFO < int(pm) - 1:
                            FIFO += 1
                        else:
                            FIFO = 0
    if token == '1':
        for line in inputFile:
            process, location = line.split(',')
            location = location.strip('0x')
            found = False

            for k in pmTable:
                if pmTable[k][0] == location:
                    pmTable[k][2] += 1
                    found = True
                elif int(k) == int(pm) - 1 and not found and pmTable[k][0] != '':
                    leastUsedNum = sys.maxsize
                    leastUsedK = ''
                    for key in pmTable:
                        if pmTable[key][2] < leastUsedNum:
                            leastUsedNum = pmTable[key][2]
                            leastUsedK = key

                    #print(line + ' = ' + 'Process ' + process + ' accesses line ' + leastUsedK)
                    pmTable[leastUsedK][0] = location
                    pmTable[leastUsedK][2] = 0
            
                    



