import os

name = './vm_snapshots/'
files = [name+'sim_0_3_512_256.dat', name+'sim_1_5_1024_256.dat', name+'sim_2_5_1024_512.dat', name+'sim_3_5_1024_768.dat', name+'sim_4_10_1024_256.dat', name+'sim_5_10_1024_512.dat']

#PCB[0] = name, PCB[1] = last access, PCB[2] = access count
memoryInfo = ['',0, 0]

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
    pmTable[str(x)] = memoryInfo

inputFile = inputFile.read()
inputFile = inputFile.split(' ')

for line in inputFile:
    process,address = line.split(',')
    print(process)

