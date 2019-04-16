from math import pow
from math import log2
import sys
import os
from random import seed 
from random import shuffle
from random import randint

# Help to format a binary string 
# important: "width" = bits in address space


def str_binary(n,padd=12):
    binfrmt = '{fill}{align}{width}{type}'.format(fill='0', align='>', width=padd, type='b')
    n = format(n,binfrmt)
    return n

def rand_address(vm_size=4096):

    bits = int(log2(vm_size))
    hbase = int(vm_size*.8)
    lbase = int(vm_size*.3)
    highlow_chances = [1,1,1,0,0,0,0,0,0,0]

    shuffle(highlow_chances)
    highlow = highlow_chances[0]

    address = 0

    if highlow > 0:
        address = randint(hbase,vm_size-1)
    else:
        address = randint(0,lbase)

    return str_binary(address,bits)

def rand_instruction(vm_size=4096):
    
    size = int(log2(vm_size))
    highlow_chances = [1,1,1,0,0,0,0,0,0,0]
    bits = ['0','1']

    shuffle(highlow_chances)
    highlow = highlow_chances[0]

    instruction = 0

    for bit in range(size):
        shuffle(bits)
        instruction += bits[0]
    return str_binary(instruction,size)

def write_sim_file(process_instructions,sim_num,np,vm,pm):
    name = "sim_{}_{}_{}_{}.dat".format(sim_num,np,vm,pm)

    f = open(os.path.join('vm_snapshots',name),"w")

    for p in process_instructions:
        f.write("{},{} ".format(p[0],hex(int(p[1], 2))))

    f.close()

def gen_addresses(minimum_instructions,max_instructions,np,vm):
    process_addresses = []

    for p in range(np):
        num_inst = randint(minimum_instructions,max_instructions)
        #sys.stdout.write("\t\t"+str(num_inst)+"\n")
        for x in range(num_inst):
            process_addresses.append((p,rand_address(vm)))

    shuffle(process_addresses)
    return process_addresses

if __name__=='__main__':

    # Address allocation within address space
    #      +-------+
    #      | stack |
    #      |       |
    #      | empty |
    #      |       |
    #      | heap  |
    #      | data  |
    #      | code  |
    #      +-------+
    seed(345678)

    virt_mem_list = [1024,2048,4096,8192]
    num_processes_list = [5,10,25,50,75,100]
    physical_mem_size = [.25,.5,.75]


    minimum_instructions = 512
    max_instructions = int(pow(2,17))

    sim_num = 0

    process_instructions = gen_addresses(minimum_instructions,max_instructions,3,512)
    write_sim_file(process_instructions,sim_num,3,512,256)

    sim_num += 1

    for vm in virt_mem_list:
        for np in num_processes_list:
            for ratio in physical_mem_size:
                pm = int(ratio*vm)
                print("{} \t{} \t{}".format(vm,np,pm))
                process_instructions = gen_addresses(minimum_instructions,max_instructions,np,vm)
                write_sim_file(process_instructions,sim_num,np,vm,pm)
                sim_num += 1

    # for vm in virt_mem_list:
    #     sys.stdout.write(str(vm)+"\n")
    #     for np in num_processes_list:
    #         sys.stdout.write("\t"+str(np)+"\n")

    #         process_instructions = gen_addresses(minimum_instructions,max_instructions,np,vm)
    #         write_sim_file(process_instructions,sim_num,np,vm)
    #         sim_num += 1
            