
memory = []

start_address_identify = 0
start_address = ""
address = 0

#initializing 64k memory 
for i in range(0, 64*1024):
        memory.append(0)

def loader(file):

        #Global variable access
        global start_address_identify
        global start_address
        global memory
        global memory_content
        global address
        #-----
        
        f = file
        # I/O -  Read the file
        try:
                with open(f) as load:
                        loader = load.readlines()
        except FileNotFound:
                print("File read error")

        # Loader - Loads the data into Instruction memory
        for i in range(0, len(loader)):
                if(loader[i][0] == "@"):                                        # @ - Points to the address
                        address_str = loader[i][1:]             
                        address = int(address_str, 8)
                elif(loader[i][0] == "-"):
                        data_binary = '{0:016b}'.format(int(loader[i][1:], 8))
                        memory[address] = int(data_binary[8:16], 2)              # loading the data to the address
                        address = address + 1
                        memory[address] = int(data_binary[0:8], 2)
                        address = address + 1
                elif(loader[i][0] == "*"):
                        start_address_identify = 1
                        start_address = loader[i][1:]
                else:
                        print("Unknown symbol found:" + loader[i][0])

'''
# Debug addition
loader()
temp_rem1 = '{0:08b}'.format(memory[address-1])
temp_rem2 = '{0:08b}'.format(memory[address-2])
print(temp_rem1 + temp_rem2 + '---' + data_binary)
print(oct(int(temp_rem1 + temp_rem2, 2) ) + " address =" + oct(address-2))
print("\n --------------------------------------------\n")
'''
