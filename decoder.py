#opcode decode
def opcode_decoder(IR):	# IR -> integer aurgument
        IR_oct = '{0:06o}'.format(IR)
        #print("IRDecode - ", IR_oct)
        if(IR_oct[1] == '0'):
                #Zero-operand instruction
                if(IR_oct[0:5] == '00000' or (IR_oct[0:4] == '0002' and IR_oct[4] != '0')):
                        IR_type = "zero_operand"
                
                #one-operand instructions
                elif(IR_oct[2] == '5' or IR_oct[2] == '6' or IR_oct[2:4] == '03'):
                        IR_type = "one_operand"
                        
                #Jump & subroutine instructions
                #JSR
                elif(IR_oct[2] == '4'):
                        IR_type = "JSR"
                
                #JMP
                elif(IR_oct[0:4] == '0001'):
                        IR_type = "JMP"
                        
                #RTS
                elif(IR_oct[0:5] == '00020'):
                        IR_type = "RTS"

                #Branch instructions
                else:
                        IR_type = "branch"
                        
        # Two-operand instructions
        else:
                IR_type = "two_operand"
                
        return IR_type
        
'''
#Debug
#File handling to test the opcode decoder 
file = open("ins.txt", "r")
lines = file.readlines()

ir = []
for i in range(len(lines)):
  ir.append(int(lines[i],8))

for i in range(len(ir)):
    result = opcode_decoder(ir[i])
    print(lines[i] + ":" + result)	
'''
