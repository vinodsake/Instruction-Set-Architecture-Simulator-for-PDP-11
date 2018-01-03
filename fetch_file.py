'''
File: Fetch.py
Purpose:
    Get the start address from the user if not specified
    
    Fetch the instruction
    Update the PC
    Call Execute Function
'''

import loader_file
import memory_access

from memory_access import *

# Importing Global variables from loader
start_address_identify = loader_file.start_address_identify
start_address = loader_file.start_address

#Declaring Instruction Register
IR = 0

def get_start_addr(startAddr):

    #Global variable access
    global IR
    global start_address
    global start_address_identify
    #-------
    
    if(startAddr != ""):
        write_data(7, int(startAddr, 8), "0", "reg_file")
        #IR = read_data(int(startAddr, 8), "0", "memory")
    elif(start_address_identify == 1):
        #start_address = "000010"
        write_data(7, int(start_address, 8), "0", "reg_file")           # Write the start_address to the program counter
    else:
        return 0
        #print("Start address - IR", oct(IR))
    return 1

def fetch():

    #Global variable access
    global IR
    # -----
    
    address_in_PC = 0
    address_in_PC = read_data(7, "0", "reg_file")                   # Reading the address present in PC
    IR  = read_data(address_in_PC, "0", "instruction_fetch")                   # Fetching from the address_in_PC and storing it in the Instruction Register
    NPC = address_in_PC + 2                                         # Incrementing the PC address by 2

    write_data(7, NPC, "0", "reg_file")                             # Update the PC with the next instruction
    #print("\n Fetch - IR =", oct(IR))
    #print("PC =", oct(address_in_PC))
    return

'''
#Debug code
write_data(255, 45, "0", "memory")
get_start_addr()
fetch()
'''
