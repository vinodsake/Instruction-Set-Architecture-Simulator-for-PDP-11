from tkinter import Tk
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import StringVar
from tkinter import Listbox
from tkinter import filedialog
from tkinter import Text
from tkinter import messagebox
import ntpath
import loader_file
import fetch_file
import main

from loader_file import *
from fetch_file import *
from execute import *
from main import *

fileName = ""
ascii_load = 0
next_step = 0

def submitObjecFile():
        print("Submited Object File")
        
        #To disable button after one click.
        okayButton.state(["disabled"])

def exitProgram():
        global selected
        
        selected.set('yes')
        display_update()
        selected.set('no')
        trace_recorder.trace_close()
        button_text.set("Done")
        okay_button.state(["disabled"])
        return

def singleStep():
        if(selected.get() == 'yes'):
                next_step= 1
                print("Single Step selected")
                button_text.set("Next Step")
        else:
                next_step= 0
                button_text.set("Okay")
                print("Single step deselected")

def Restart():
        global ascii_load
        global next_step
        global mbreak
        
        ascii_load = 0
        next_step = 0
        trace_recorder.trace_close()    # Close the trace file on restart

        # Open the trace files
        trace_recorder.trace_file = open('trace_record.txt', 'w')
        trace_recorder.branch_file = open('branch_record.txt', 'w')

        # Deleting the display in the GUI
        reg_content.delete(0,'end')
        NZVC_content.delete(0, 'end')
        irEntry.delete(0, 'end')
        memory_content.delete(0, 'end')
        statistics_text.delete(0, 'end')
        branch_trace_content.delete(0, 'end')
        trace_file_content.delete(0, 'end')
        mbreak.set("")
        startAddr.set("")

        # Deleting the instruction count
        trace_recorder.instruction_count= 0

        # Clearing the Start address
        loader_file.start_address_identify = 0
        loader_file.start_address = ""
        
        # Deleting temporary storage spaces in trace_recorder
        del trace_recorder.address_accessed[0:]
        del trace_recorder.branch_encountered[0:]        

        # Enabling the start button
        okay_button.state(["!disabled"])

        # Clearing the registers
        memory_access.clear_reg()

        # Clearing the NZVC
        NZVC_clear()
        
        booter()
        return

def booter():
        global ascii_load
        global fileName
        global startAddr
        global next_step

        #fileName.set("fib_ascii.txt")
        if(fileName.get() == ''):
                messagebox.showerror(message = 'Please give the ASCII File', title = 'Error')
                return
        else:
                if(ascii_load == 0):
                        print("File Name = ", fileName.get(), end = "\n")
                        loader_file.loader(fileName.get())
                        startAddr.set(loader_file.start_address)
                        for i in range(0, 64*1024-1, 2):
                                byte0 = loader_file.memory[i]
                                i = i+1
                                byte1 = loader_file.memory[i]
                                word = int(('{0:08b}'.format(byte1) + '{0:08b}'.format(byte0)), 2)   # binary concatenation to obtain 16 bits 
                                memory_content.insert('end', 'Mem[%s] -> %s' % ('{0:06o}'.format(i-1), '{0:06o}'.format(word)))
                        #print("startAddr = ", startAddr.get(), end = "\n")
                        button_text.set("Start!")
                else:
                        if(next_step == 0):
                                checkStartAddr()
                        else:
                                pipeline()
                                print("Called Pipeline")
                        return
                ascii_load = 1
                return 

def checkStartAddr():
        global startAddr
        global next_step

        start = get_start_addr(startAddr.get())
        if(start == 0):
                print("No starting address given!")
                messagebox.showerror(message='No starting address given!', title='Error')
        else:
                print("Starting address=",startAddr.get())
                next_step = 1
                pipeline()

def display_update():
        global reg_names
        global trace_file_text

        reg_content.delete(0,'end')
        NZVC_content.delete(0, 'end')
        memory_content.delete(0, 'end')
        statistics_text.delete(0, 'end')

        # Updating the Registers
        for i in range (0, 6, 1):
                reg_content.insert('end', 'reg[%d] -> %s' % (i, read_reg(i)))
        reg_content.insert('end', 'SP -> %s' % (read_reg(6)))
        reg_content.insert('end', 'PC -> %s' % (read_reg(7)))

        # Updating the NZVC
        psw = update_psw()
        NZVC_content.insert('end', 'N -> %s, Z -> %s, V -> %s, C -> %s' % (psw[0], psw[1], psw[2], psw[3]))
        
        # Updating the Instruction Register
        ir.set('{0:06o}'.format(fetch_file.IR))

        statistics_text.insert('end', trace_recorder.instruction_count)
        
        #Updating the trace file
        for i in range(0, len(trace_recorder.address_accessed)):
                trace_file_content.insert("end", trace_recorder.address_accessed[i])
        del trace_recorder.address_accessed[0:]

        #Updating the Branch trace
        for i in range(0, len(trace_recorder.branch_encountered)):
                branch_trace_content.insert("end", trace_recorder.branch_encountered[i])
        del trace_recorder.branch_encountered[0:]
        
        #Updating the memory
        if(selected.get() == 'yes' or mbreak.get() == memory_access.read_reg(7)):
                for i in range(0, 64*1024-1, 2):
                        byte0 = loader_file.memory[i]
                        i = i+1
                        byte1 = loader_file.memory[i]
                        word = int(('{0:08b}'.format(byte1) + '{0:08b}'.format(byte0)), 2)   # binary concatenation to obtain 16 bits 
                        if(main.debug == "ON"):
                                if(i-1 == 0):
                                        print(word)
                        memory_content.insert('end', 'Mem[%s] -> %s' % ('{0:06o}'.format(i-1), '{0:06o}'.format(word)))

        return
       
def saveFileName():
        global fileName
        
        fileName.set(ntpath.basename(filedialog.askopenfilename()))
        
#Define root window
root= Tk()

#Give title for the window
root.title("PDP-11/20 ISA Simulator")

#Disable resize of the window
root.resizable(width=False, height=False)

#Define a frame. This will hold other widgets. Size of frame depends on
#what's inside the frame or explicitly mention using height/width.
frame= ttk.Frame(root)

#Give some padding around the inside of the frame.
frame['padding'] = (10)

#Change borderwidth of the widgets inside the frame and its visual appearance
#frame['borderwidth'] = 2
#frame['relief'] = 'sunken'

label1= ttk.Label(frame, text= "Give Object File")
#label2= ttk.Label(frame, text= "Name2")
#label2.grid()

#To display image
#image = PhotoImage(file='workstation.png')
#label2['image'] = image

#To create a button
#okayButton= ttk.Button(frame, text='Okay', command=submitObjecFile)
cancelButton= ttk.Button(frame, text= 'Reboot', command= Restart)
#This will do the button click action for you
#button.invoke()

#checkbuttons
selected = StringVar()

singleStepCheck = ttk.Checkbutton(frame, text='Single Step', 
            command=singleStep, variable= selected,
            onvalue='yes', offvalue='no')
                
#Entries
startAddrLabel= ttk.Label(frame, text= 'Starting Address')
startAddr= StringVar()
button_text= StringVar()
addr = ttk.Entry(frame, width= 16, textvariable=startAddr)
okay_button= ttk.Button(frame, textvariable= button_text, command= booter)
button_text.set("Load ASCII File")

fileName= StringVar()
fileNameLabel= ttk.Label(frame, text= 'ASCII File')
fileNameEntry= ttk.Entry(frame, width= 27, textvariable= fileName)
fileNameButton= ttk.Button(frame, text= 'Browse', command= saveFileName)

#Contributers 
authorNames= ttk.Label(frame, text= 'Project by\nBharath, Pradeep and Vinod.\n\nECE 586, Prof. Mark G. Faust')
authorNames.config(font=("Courier", 10))

reg_names= ()
#reg_names= {'reg0 ->': '', 'reg1 ->': '', 'reg2 ->': '', 'reg3 ->': '', 'reg4 ->':'', 'reg5 ->':'', 'sp ->':'', 'pc ->':''}
reg_file= StringVar(value= reg_names)

#Listboxes - Register and Memory 
memory_content = Listbox(frame, height= 17, width= 25)
reg_content= Listbox(frame, height= 8, width= 16, listvariable= reg_file)

NZVC= StringVar()
#Listboxes
NZVC_content= Listbox(frame, height= 1, width= 27, listvariable= NZVC)

#Empty Frame
branchFrame= ttk.Frame(frame)

#Instruction Register
ir = StringVar()
irLabel= ttk.Label(frame, text= 'Instruction Register')
irEntry= Listbox(frame, height= 1, width= 16, listvariable=ir)

# Memory breakpoint
mbreak = StringVar()
mbreakLabel= ttk.Label(frame, text= 'Break Point')
mbreakEntry= ttk.Entry(frame, width= 16, textvariable=mbreak)

#Scrollbar for listboxes
memory_content_scrollBar = ttk.Scrollbar( frame, orient="vertical", command=memory_content.yview)
memory_content.configure(yscrollcommand= memory_content_scrollBar.set)

memory_content_label= ttk.Label(frame, text= "Memory Contents")
reg_content_label= ttk.Label(frame, text= "Register Contents")
NZVC_content_label= ttk.Label(frame, text= "NZVC Flags")

#Listbox to display trace file
trace_file_content= Listbox(frame, width= 30, height= 17)
trace_file_scrollBar = ttk.Scrollbar( frame, orient="vertical", command=trace_file_content.yview)
trace_file_content.configure(yscrollcommand=trace_file_scrollBar.set)
trace_file_label= ttk.Label(frame, text= 'Memory Trace')

#Listbox to display branch trace file
branch_trace_content= Listbox(frame, width= 34, height= 12)
branch_trace_scrollBar = ttk.Scrollbar( frame, orient="vertical", command=branch_trace_content.yview)
branch_trace_content.configure(yscrollcommand=branch_trace_scrollBar.set)
branch_trace_label= ttk.Label(frame, text= "Branch Trace")
branch_trace_header= ttk.Label(frame, text="PC, branch, target PC, taken")

#Text box to display statistics
statistics_text= Listbox(frame, width= 16, height= 1)
statistics_label= ttk.Label(frame, text= 'Instruction Count')

#Call geometry manager. This will put the widgets onscreen.
frame.grid()

authorNames.grid(column= 6, row= 17, sticky= 'W', padx= 5, pady= 5, columnspan= 2, rowspan= 4)

fileNameLabel.grid(column= 6, row= 15, sticky= 'W', pady= (5,0), padx= (5,5))
fileNameEntry.grid(column= 6, row= 16, sticky= 'W', pady= (0,5), padx= (5,0), columnspan=1)
fileNameButton.grid(column= 7, row= 16, sticky= 'W', pady= (0,5), padx= (0,5))

startAddrLabel.grid(column= 0, row= 13, sticky= 'W', padx=5)
addr.grid(column= 0, row= 14, sticky= 'W', pady=(0, 5), padx=5)

okay_button.grid(column= 1, row= 19, sticky= 'W', pady=5, padx=5)

cancelButton.grid(column= 3, row= 19, sticky= 'W', pady=5, padx=5)

singleStepCheck.grid(column= 0, row= 17, sticky= 'WE', pady=5, padx=5)

mbreakLabel.grid(column= 0, row= 15, sticky= 'W', pady= (5,0), padx= 5)
mbreakEntry.grid(column= 0, row= 16, sticky= 'W', pady= (0,5), padx= 5)

memory_content_label.grid(column= 1, row= 0, sticky= 'W', padx= 5, pady= (5, 0))
memory_content.grid(column= 1, row= 1, sticky= ('W','E','N','S'), padx= (5,0), pady= (0,5), columnspan= 1, rowspan= 17)
memory_content_scrollBar.grid(column= 2, row= 1, sticky=('W','N','S'), pady= (0,5), padx=(0,5), rowspan= 17)

reg_content_label.grid(column= 0, row= 0, sticky= 'W', pady= (5,0), padx=5)
reg_content.grid(column= 0, row= 1, sticky= 'W', pady= (0,5), padx= 5, rowspan= 8)

irLabel.grid(column= 0, row= 9, sticky= 'W', pady= (5,0), padx= 5)
irEntry.grid(column= 0, row= 10, sticky= 'W', pady= (0,5), padx= 5)

trace_file_label.grid(column= 3, row= 0, sticky= 'WE', padx=5, pady= (5,0))
trace_file_content.grid(column= 3, row= 1, sticky= ('W','E','N','S'), padx= (5,0), pady= (0,5), rowspan= 17, columnspan=2)
trace_file_scrollBar.grid(column= 5, row= 1, sticky=('W','N','S'), pady= (0,5), rowspan= 17, padx=(0,5))

branch_trace_label.grid(column= 6, row= 0, sticky= 'W', padx=5, pady= (5,0))
#branch_trace_header.grid(column= 6, row= 1, sticky=('W'), padx= 5)
branch_trace_content.grid(column= 6, row= 1, sticky= ('W','N','S','E'), padx= (5,0), pady= (0,5), rowspan= 12, columnspan=2)
branch_trace_scrollBar.grid(column= 8, row= 1, sticky=('W','N','S'), pady= (0,5), padx= (0,5), rowspan= 12)

statistics_label.grid(column= 0, row= 11, sticky= 'W', pady= (5,0), padx= 5)
statistics_text.grid(column= 0, row= 12, sticky= ('W'), padx= 5, pady= (0,5))

NZVC_content_label.grid(column= 6, row= 13, sticky= 'W', pady= (5,0), padx=5)
NZVC_content.grid(column= 6, row= 14, sticky= 'W', pady= (0,5), padx= 5, rowspan= 1)

root.mainloop()
