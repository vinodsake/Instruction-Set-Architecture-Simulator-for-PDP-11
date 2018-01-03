'''
File: main.py
Purpose:
    Main module implements the pipeline by calling the functions
'''
"K:/PSU/Computer Architecture/PDP11/fib_ascii.txt"
import loader_file
import fetch_file
import trace_recorder
import gui

from loader_file import *
from fetch_file import *
from memory_access import *
from decoder import * 
from find_eff_addr import *
from execute import *
from gui import *

debug = "OFF"

# Start of the process

'''
Loader and Get Start Address handled by GUI

loader()                    # Trigger the loader to copy the instructions into memory

get_start_addr()            # Starting address of the program
'''

def pipeline():
    
    while(1):
        fetch()
        if(debug == "ON"):
            print("fetch done")
        if(fetch_file.IR == 0):
                print("Program Execution Complete")
                gui.exitProgram()       # Function imported from GUI
                break
        else:
                instruction_type = opcode_decoder(fetch_file.IR)
                if(debug == "ON"):
                    print("decode done")
                execute(instruction_type)
                if(debug == "ON"):
                    print("Execute Done")
        gui.display_update()
        if(gui.selected.get() == "yes" or gui.mbreak.get() == read_reg(7)):
            break
