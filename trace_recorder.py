'''
File Name: trace_recorder
Purpose: The purpose of the file is to write to the trace file about memory reads and writes

Functions:
  trace_record(int type, octal address)
    type:
        0 - Data Read
        1 - Data Write 
        2 - Instruction Fetch
    octal address:
        address accessed from memory (representation: octal)

  branch_record(PC, branch, target_address, Branchtaken)
    PC: instruction PC
    branch: Type of branch instruction (ISA)
    target_address: next address
    branchtaken: Branch Taken or Not Taken
'''

try:
    trace_file = open('trace_record.txt', 'w')
except:
    print("Trace file creation error")

try:
    branch_file = open('branch_record.txt', 'w')
except:
    print("Branch trace file creation error")

address_accessed = []
branch_encountered = []
instruction_count = 0
    
def trace_record(type_access, address_int):
    #Global section
    global trace_file
    global address_accessed
    global instruction_count

    address = '{0:06o}'.format(address_int)
    
    if(type_access == 0):
        value = (type_access, address, "Data Read")
        s = str(value)
        trace_file.write(s)
        trace_file.write("\n")
        address_accessed.append(s)        
    elif(type_access == 1):
        value = (type_access, address, "Data Write")
        s = str(value)
        trace_file.write(s)
        trace_file.write("\n")
        address_accessed.append(s)
    else:
        value = (type_access, address, "Instruction Fetch")
        s = str(value)
        trace_file.write(s)
        trace_file.write("\n")
        address_accessed.append(s)
        instruction_count = instruction_count + 1
    return

def branch_record(PC, branch, target_address, branchtaken):
    #Global section
    global branch_file
    global branch_encountered
    #----
    
    if(branchtaken == 1):
        T_NT = "Taken"
    else:
        T_NT = "Not Taken"
        
    value = ('{0:06o}'.format(PC), branch, '{0:06o}'.format(target_address), T_NT)
    s = str(value)
    branch_file.write(s) 
    branch_file.write("\n")
    branch_encountered.append(s)
    return

def trace_close():
    #Global section
    global trace_file
    global branch_file
    #----

    trace_file.close()
    branch_file.close()
    return 
