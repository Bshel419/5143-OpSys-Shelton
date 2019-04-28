#ADV OS SYSTEMS-A04-Benjamin Shelton
#This program opens various input files containing processes calling for memory location to be loaded into
#physical memory. It compares 4 different types of paging algorithms (FIFO, Least Recently Used, Least Frequently Used, Random replacement),
#and displays the number of page faults of each using a bar graph.
#PS: The first file is always a little wonky. I don't know why. But after the first file the rest go smoothly. Also the program works well on my laptop
#but for some reason messes up sometimes on my desktop. If your PC happens to hate it like my desktop then I can run it in your office or something.
#Also it likes to hang sometimes.
import os
import sys
import random
import numpy as np
import matplotlib.pyplot as plt

#function to clear physical memory
def clearDict(d):
    for k in d:
        d[k] = ['', 1, 0]

if __name__ == '__main__':
    name = './vm_snapshots/'
    
    #list that holds all of the input files
    files = os.listdir('./vm_snapshots')

    #append the vm_snapshot directory to the names of each file
    for x in range(len(files)):
        files[x] = name + files[x]
    
    print("0: Run the whole darn thing (all files in vm_snapshots. Takes forever. Also will have to exit out of bar graph for each file in order to get to the next one.)")
    print("1: Run the program for a specific file (exact file name required. Will append /vm_snapshots/ to the file name)")
    choice = input("What would you like to do? (Choose either 0 or 1): ")

    if choice == '0':
        for fi in files:
            p = fi            # path to file
            f = os.path.basename(p)                             # get basename (remove path)
            name, ext = f.split('.')                            # split name from extension
            s,run,np,vm,pm = name.split('_')  # get each piece of info

            inputFile = open(p, 'r')

            pmTable = {}
            #holds number of page faults for each algorithm in order to graph them at the end
            page_faults = []

            for x in range(int(pm)):
                #[0] = name, [1] = access count, [2] = last access
                pmTable[str(x)] = ['', 1, 0]

            inputFile = inputFile.read()
            inputFile = inputFile.split(' ')
            #space at the end of every file that would cause an error. So pop that space out.
            inputFile.pop(len(inputFile) - 1)


            #-----------------------------------------------------------------------------------------------------
            #FIFO
            page_fault = 0
            #itterator that keeps track of which slot of physical memory is next to be swapped out
            FIFO = 0
            for line in inputFile:
                process, location = line.split(',')
                location = location.strip('0x')
                
                found = False 
                #if the address is already in memory then no need to worry about swapping
                for k in pmTable:
                    if pmTable[k][0] == location:
                        found = True

                if not found:
                    pmTable[str(FIFO)][0] = location
                    print(line + ' = ' + 'Process ' + process + ' accesses line ' + str(FIFO))
                    page_fault += 1
                    #prevents the counter from getting larger than physical memory
                    if FIFO < int(pm) - 1:
                        FIFO += 1
                    else:
                        FIFO = 0
            page_faults.append(page_fault)
            #---------------------------------------------------------------------------------------------------
            #Least Recently Used
            clearDict(pmTable)
            page_fault = 0
            #had to set it to -1 because I had to check the pmTable before running the algorithm and if it was 0 then it would put the first memory location in spot 1
            initialize = -1
            time = 0

            for line in inputFile:
                process, location = line.split(',')
                location = location.strip('0x')
                
                found = False
                #same as FIFO, if it's in there then we don't need to worry about swappping
                for k in pmTable:
                    if pmTable[k][0] == location:
                        found = True
                #if it's in there before we've fully initialized physical memory then we don't want it to double up
                if not found:
                    initialize += 1
                #had to reset found so that way we can update last access 
                found = False
                
                for k in pmTable:
                    #since we loop through the whole table found can be true after the first page we check, so have to add the not found stipulation
                    if pmTable[k][0] == location and not found:
                        pmTable[k][2] = time
                        found = True
                    #if it's not physical memory and we've reached the end and we've already intiialized physical memory
                    elif int(k) == int(pm) - 1 and not found and initialize >= int(pm):
                        #simple "find lowest number in a list" algorithm, along with saving the key
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
                        #prevents adding the same location for the rest of the dictionary after we've added it (added it in pmTable['3']...we still have like 1000 more keys to go)
                        found = True
                    elif initialize < int(pm) and not found:
                        #if the physical memory is still missing some slots
                        pmTable[str(initialize)][0] = location
                        pmTable[str(initialize)][2] = time
                        print(line + ' = ' + 'Process ' + process + ' accesses line ' + str(initialize))
                        page_fault += 1
                        found = True
                time += 1

            page_faults.append(page_fault)
            #------------------------------------------------------------------------------------------------------
            #Least Frequently Used-Very similar to LRU
            clearDict(pmTable)
            page_fault = 0
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
                        #except we keep track of number of accesses
                        pmTable[k][1] += 1
                        pmTable[k][2] = time
                        found = True
                    elif int(k) == int(pm) - 1 and not found and initialize >= int(pm):
                        leastUsedNum = 0
                        leastUsedK = ''
                        for key in pmTable:
                            #and the comparison is a bit different
                            if pmTable[key][1]/pmTable[key][2] > leastUsedNum:
                                leastUsedNum = pmTable[key][1]/pmTable[key][2]
                                leastUsedK = key
                        print(line + ' = ' + 'Process ' + process + ' accesses line ' + leastUsedK)
                        page_fault += 1
                        pmTable[leastUsedK][0] = location
                        pmTable[leastUsedK][1] = 1
                        pmTable[leastUsedK][2] = time
                        found = True
                    elif initialize < int(pm) and not found:
                        pmTable[str(initialize)][0] = location
                        pmTable[str(initialize)][2] = time
                        print(line + ' = ' + 'Process ' + process + ' accesses line ' + str(initialize))
                        page_fault += 1
                        found = True
                time += 1

            page_faults.append(page_fault)    
            #------------------------------------------------------------------------------------------------------
            #Random
            clearDict(pmTable)
            page_fault = 0
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
                            #grab a random slot to throw the memory location in
                            r = random.randint(0, int(pm) - 1)
                            print(line + ' = ' + 'Process ' + process + ' accesses line ' + str(r))
                            page_fault += 1
                            pmTable[str(r)][0] = location

            page_faults.append(page_fault)
            #----------------------------------------------------------------------------------------------
            #pyplot stuff
            plt.style.use('ggplot')

            x = ['FIFO', 'LRU', 'LFU', 'Random']

            x_pos = [i for i, _ in enumerate(x)]

            plt.bar(x_pos, page_faults, color='green')
            plt.xlabel("Algorithms")
            plt.ylabel("Page Faults")
            plt.title(fi.strip(name))

            plt.xticks(x_pos, x)

            plt.show()
    #second verse same as the first but just with a single file rather than looping through all files
    elif choice == '1':
        p = input("Input file name: ")
        p = name + p
        try:           # path to file
            f = os.path.basename(p)                             # get basename (remove path)
            name, ext = f.split('.')                            # split name from extension
            s,run,np,vm,pm = name.split('_')  # get each piece of info

            inputFile = open(p, 'r')

            pmTable = {}

            page_faults = []

            for x in range(int(pm)):
                #[0] = name, [1] = access count, [2] = last access
                pmTable[str(x)] = ['', 0, 1]

            inputFile = inputFile.read()
            inputFile = inputFile.split(' ')
            inputFile.pop(len(inputFile) - 1)



            #-----------------------------------------------------------------------------------------------------
            #FIFO
            page_fault = 0
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
            page_faults.append(page_fault)
            #---------------------------------------------------------------------------------------------------
            #Least Recently Used
            clearDict(pmTable)
            page_fault = 0
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

            page_faults.append(page_fault)
            #------------------------------------------------------------------------------------------------------
            #Least Frequently Used
            clearDict(pmTable)
            page_fault = 0
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
                        leastUsedNum = 0
                        leastUsedK = ''
                        for key in pmTable:
                            if pmTable[key][1]/pmTable[key][2] > leastUsedNum:
                                leastUsedNum = pmTable[key][1]/pmTable[key][2]
                                leastUsedK = key
                        print(line + ' = ' + 'Process ' + process + ' accesses line ' + leastUsedK)
                        page_fault += 1
                        pmTable[leastUsedK][0] = location
                        pmTable[leastUsedK][1] = 1
                        pmTable[leastUsedK][2] = time
                        found = True
                    elif initialize < int(pm) and not found:
                        pmTable[str(initialize)][0] = location
                        pmTable[str(initialize)][2] = time
                        print(line + ' = ' + 'Process ' + process + ' accesses line ' + str(initialize))
                        page_fault += 1
                        found = True
                time += 1

            page_faults.append(page_fault)    
            #------------------------------------------------------------------------------------------------------
            #Random
            clearDict(pmTable)
            page_fault = 0
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

            page_faults.append(page_fault)
            #----------------------------------------------------------------------------------------------
            plt.style.use('ggplot')

            x = ['FIFO', 'LRU', 'LFU', 'Random']

            x_pos = [i for i, _ in enumerate(x)]

            plt.bar(x_pos, page_faults, color='green')
            plt.xlabel("Algorithms")
            plt.ylabel("Page Faults")
            plt.title(p.strip(name))

            plt.xticks(x_pos, x)

            plt.show()
        except:
            print("ERROR: File name not correct.")
    else:
        print("ERROR: Incorrect input entered.")









