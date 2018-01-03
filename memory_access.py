'''
File: memory_access.py
Purpose: Read/ Write functions from the memory/ register file
Accessing functions:

Reading data:
read_data( address(int), byte_op(string), memory_read(string) )

byte_op = "1" - Fetch a single byte
        = "any other string" - Fetches a single word
memory_read = "memory" - Fetches the data from memory
            = "reg_file" - Fetches the data from register file
To access from reg_file,
    address range is (0, 7).
    Any other address will popup an error.

Writing data:
write_data(address_write(int), data_write(int), byte_op(string), memory_write(string))


byte_op and memory_write works the same way as read
data_write -
    If it is greater than 8 bits for byte operation, only the LSB 8 bits are stored
    If it is greater than 16 bits for word operation, only the LSB 16 bits are stored
    carry or overflows are ignored
'''

import trace_recorder
import loader_file
from trace_recorder import *

memory = loader_file.memory         ### Use this memory variable for the GUI

# Register class
# The low and high variables represent the lower 8 bits and higher 8 bits of the register respectively
class register:
    __low = 0
    __high = 0

    def __init__(self):
        self.__low = 0
        self.__high = 0

    def write_low(self, value):
        if(value > 255):
            self.__low = value - 256
        else:
            self.__low = value
            
    def write_high(self, value):
        if(value > 255):
            self.__high = value - 256
        else:
            self.__high = value
    def read_low(self):
        return self.__low
    def read_high(self):
        return self.__high
    def clear(self):
        self.__low = 0
        self.__high = 0
        return
# --- End of Register class ---

# Declaring the Register file
class reg_file:
    R = []
    for i in range(0,8):
        R.append(register())
    
def read_data(address_read, byte_op, memory_read):

    #Global variable access
    global memory
    #-----
    
    if(address_read >= 64*1024):
        address_read = address_read - 64*1024
        
    if(memory_read == "memory" or memory_read == "instruction_fetch"):

        # Writing to the trace file - Memory reads and Instruction Fetches
        if(memory_read == "memory"):
            trace_record(0, address_read)
        else:
            trace_record(2, address_read)
        #----
            
        if(byte_op == "1"):
            return memory[address_read]                                             # Returning the byte in the memory location
        else:
            access1 = memory[address_read]                                          # accessing the word from consecutive memory locations               
            access2 = memory[address_read + 1]
            binary_concat = '{0:08b}'.format(access2) + '{0:08b}'.format(access1)   # binary concatenation to obtain 16 bits 
            data_out = int(binary_concat, 2)                                        # data_out contains the word
            return data_out
    else:
        if(byte_op == "1"):
            return reg_file.R[address_read].read_low()
        else:
            access1 = reg_file.R[address_read].read_low()                           # address_read is the register address in the register file
            access2 = reg_file.R[address_read].read_high()                          # It ranges from 0 to 7 (SP = 6, PC = 7)
            binary_concat = '{0:08b}'.format(access2) + '{0:08b}'.format(access1)   # binary concatenation to obtain 16 bits 
            data_out = int(binary_concat, 2)                                        # data_out contains the word
            return data_out

def write_data(address_write, data_write, byte_op, memory_write):

    #Global variable access
    global memory
    #-----
    
    if(address_write >= 64*1024):
        address_write = address_write - 64*1024
    
    if(memory_write == "memory"):
        
        # Writing to the trace file - Memory writes
        if(memory_write == "memory"):
            trace_record(1, address_write)
        #----
        if(byte_op == '1'):
            if(data_write > 255):
                data_write = data_write - 256                                       # If the data is greater than 8'b11111111, ignore the overflowing bits
            memory[address_write] = data_write
            return 1
        else:
            if(data_write > (2**16 - 1)):
                data_write = data_write - 2**16                                      # If the data is greater than 16{1'b1}, ignore the overflowing bits
            data_binary = '{0:016b}'.format(data_write)                             # Storing the word in consecutive memory locations 
            memory[address_write] = int(data_binary[8:16], 2)                       # storing the lower 8 bits to the address_write specified
            address_write = address_write + 1
            memory[address_write] = int(data_binary[0:8], 2)                        # storing the higher 8 bits to the address_write + 1 - little endian
            return 1
        
    else:
        if(byte_op == "1"):
            if(data_write > 255):
                data_write = data_write - 256                                       # If the data is greater than 8'b11111111, ignore the overflowing bits
            reg_file.R[address_write].write_low(data_write)
            return 1
        else:
            if(data_write > (2**16 - 1)):
                data_write = data_write - 2**16                                      # If the data is greater than 16{1'b1}, ignore the overflowing bits
            data_binary = '{0:016b}'.format(data_write)                             # Storing the word in the specified register
            low = int(data_binary[8:16], 2)                                         # storing the lower 8 bits to the Register Low
            high = int(data_binary[0:8], 2)                                         # storing the higher 8 bits to the Register High
            reg_file.R[address_write].write_low(low)                                # Address_write is the register address in the register file
            reg_file.R[address_write].write_high(high)                              # It ranges from 0 to 7 (Stack Pointer = 6, Program Counter = 7)
            return 1

# Read_reg is used for GUI display
# Accessing the above functions will be written to trace. Any calls to read_reg will be off the record
def read_reg(reg):
    access1 = reg_file.R[reg].read_low()                           # address_read is the register address in the register file
    access2 = reg_file.R[reg].read_high()                          # It ranges from 0 to 7 (SP = 6, PC = 7)
    binary_concat = '{0:08b}'.format(access2) + '{0:08b}'.format(access1)   # binary concatenation to obtain 16 bits
    return '{0:06o}'.format(int(binary_concat, 2))

def clear_reg():
    for i in range(0,8):
        reg_file.R[i].clear()
    return
    
'''Debug code 
write_data(7, 288, '0', "reg_file")
access1 = read_data(7, '0', 'reg_file')
print(access1)
write_data(240, 19, '0', "memory")
access1 = read_data(240, '0', "memory")
print(access1)
'''
