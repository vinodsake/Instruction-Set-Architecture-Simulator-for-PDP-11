import fetch_file
from memory_access import *
from find_eff_addr import *
from Classes.classes import opcode_c
from Classes.classes import addr_mode_c
from Classes.classes import reg_file_c
	
N = "0"
Z = "0"
V = "0"
C = "0"

def update_psw():
        psw = [N, Z, V, C]
        return psw

def NZVC_clear():
        global N
        global Z
        global V
        global C

        N = "0"
        Z = "0"
        V = "0"
        C = "0"
        
def execute(instruction_type):
        #Global variable access
        IR = fetch_file.IR
        #print("instruction_type", instruction_type)
        global N 
        global Z
        global C
        global V
        
        #One operand instructions. opcode= IR[15:6], dst= IR[5:0]
        if(instruction_type == "one_operand"):
                #Select opcode bits
                opcode= '{0:06o}'.format(IR)[0:4]
        
                #Select addressing mode bits
                addr_mode= '{0:06o}'.format(IR)[4]
        
                #Select destination bits
                dst= '{0:06o}'.format(IR)[5]
                
                #Check if byte operation
                byte_op= '{0:06o}'.format(IR)[0]
                
                #CLR{B} dst
                if(opcode == opcode_c.CLR or opcode == opcode_c.CLRB):
                        
                        result= 0
                        #If register addressing mode, clear the register
                        if(addr_mode == addr_mode_c.reg):	
                                write_data(int(dst), result, byte_op, 'reg_file')
                        #If not register addressing mode, get effective address of operand and
                        #clear the memory address
                        else:
                                eff_addr= find_eff_addr(int(dst), addr_mode, byte_op)
                                write_data(eff_addr, result, byte_op, 'memory')
                        
                        #Update NZVC bits in Processor Status word (PSW)
                        Z= '1'
                        N= '0'
                        C= '0'
                        V= '0'
                        update_psw()
                        
                #INC{B} dst
                elif(opcode == opcode_c.INC or opcode == opcode_c.INCB):
                        #Depending on byte_op, operand will have 8/16bit data from reg_file/mem
                        if(addr_mode == addr_mode_c.reg):
                                operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                eff_addr= find_eff_addr(int(dst), addr_mode, byte_op)
                                operand= read_data(eff_addr, byte_op, 'memory')
                        
                        result= operand + 1
                        
                        if(addr_mode == addr_mode_c.reg):
                                write_data(int(dst), result, byte_op, 'reg_file')
                        else:
                                write_data(eff_addr, result, byte_op, 'memory')
                        
                        #If least significant 8bits of result for byte_op or least significant 16bits of result for word_op are 0, set Z bit.
                        #If MSB (7th bit for byte_op, 15th bit for word_op) of result is 1, set 
                        #N bit.
                        #C bit is not affected.
                        #If operand= 127 (0o177) for byte_op or operand= 32767 (0o077777) for
                        #word_op, set V bit.
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                        
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                                #C not affected
                                
                                if(oct(operand) == '0o177'):
                                        V= '1'
                                else:
                                        V= '0'
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                        
                                if('{0:017b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                
                                #C not affected
                                
                                if(oct(operand) == '0o77777'):
                                        V= '1'
                                else:
                                        V= '0'
                        update_psw()
                
                #DEC{B} dst
                elif(opcode == opcode_c.DEC or opcode == opcode_c.DECB):
                        if(addr_mode == addr_mode_c.reg):
                                operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                eff_addr= find_eff_addr(int(dst), addr_mode, byte_op)
                                operand= read_data(eff_addr, byte_op, 'memory')
                        
                        #Perform 2's complement addition
                        if(byte_op == '1'):
                                result= operand + int(-1 & 2**8-1)
                        else:
                                result= operand + int(-1 & 2**16-1)
                        
                        if(addr_mode == addr_mode_c.reg):
                                write_data(int(dst), result, byte_op, 'reg_file')
                        else:
                                write_data(eff_addr, result, byte_op, 'memory')
                                                        
                        #If least significant 8bits of result for byte_op or least significant 16bits of result for word_op are 0, set Z bit.
                        #If MSB (7th bit for byte_op, 15th bit for word_op) of result is 1, set 
                        #N bit.
                        #V bit is not affected.
                        #If operand= 128 (0o200) for byte_op or operand= 32768 (0o100000) for
                        #word_op, set C bit.
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                
                                #V not affected
                                
                                if(oct(operand) == '0o200'):
                                        C= '1'
                                else:
                                        C= '0'
                                        
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                        
                                if('{0:017b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                                #V not affected
                                
                                if(oct(operand) == '0o100000'):
                                        C= '1'
                                else:
                                        C= '0'
                        
                        update_psw()
                
                #ADC{B} dst
                elif(opcode == opcode_c.ADC or opcode == opcode_c.ADCB):
                        if(addr_mode == addr_mode_c.reg):
                                operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                eff_addr= find_eff_addr(int(dst), addr_mode, byte_op)
                                operand= read_data(eff_addr, byte_op, 'memory')
                                
                        result= operand + int(C)
                        C_temp= C
                        
                        if(addr_mode == addr_mode_c.reg):
                                write_data(int(dst), result, byte_op, 'reg_file')
                        else:
                                write_data(eff_addr, result, byte_op, 'memory')
                        
                        #If least significant 8bits of result for byte_op or least significant 16bits of result for word_op are 0, set Z bit.
                        #If MSB (7th bit for byte_op, 15th bit for word_op) of result is 1, set 
                        #N bit.
                        #If operand= 0o177777 and C= 1 for word_op, operand= 0o377 and C= 1 for
                        #byte_op, set C bit.
                        #If operand= 0o077777 and C= 1 for word_op, operand= 0o177 and C= 1 for
                        #byte_op, set V bit.
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                                if(oct(operand) == '0o377' and C_temp == '1'):
                                        C= '1'
                                else:
                                        C= '0'
                                        
                                if(oct(operand) == '0o177' and C_temp == '1'):
                                        V= '1'
                                else:
                                        V= '0'
                        
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:17b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                                if(oct(operand) == '0o177777' and C_temp == '1'):
                                        C= '1'
                                else:
                                        C= '0'
                                        
                                if(oct(operand) == '0o77777' and C_temp == '1'):
                                        V= '1'
                                else:
                                        V= '0'
                        
                        update_psw()
                        
                #SBC{B} dst
                elif(opcode == opcode_c.SBC or opcode == opcode_c.SBCB):
                        if(addr_mode == addr_mode_c.reg):
                                operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                eff_addr= find_eff_addr(int(dst), addr_mode, byte_op)
                                operand= read_data(eff_addr, byte_op, 'memory')
                        
                        #Perform 2's complement addition
                        if(byte_op == '1'):
                                result= operand + int(-int(C) & 2**8-1)
                        else:
                                result= operand + int(-int(C) & 2**16-1)
                        
                        C_temp= C
                        
                        if(addr_mode == addr_mode_c.reg):
                                write_data(int(dst), result, byte_op, 'reg_file')
                        else:
                                write_data(eff_addr, result, byte_op, 'memory')
                        
                        #Z: set if the result 0; cleared otherwise
                        #N: set if the result < 0; cleared otherwise
                        #C: cleared if the result is 0 and C = 1; set otherwise
                        #V: set if the result is 100000 (word_op); cleared otherwise
                        
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                                if(Z == '1' and C_temp == '1'):
                                        C= '0'
                                else:
                                        C= '1'
                                        
                                if(oct(result) == '0o200'):
                                        V= '1'
                                else:
                                        V= '0'
                        
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:17b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                                if(Z == '1' and C_temp == '1'):
                                        C= '0'
                                else:
                                        C= '1'
                                        
                                if(oct(result) == '0o100000'):
                                        V= '1'
                                else:
                                        V= '0'
                        
                        update_psw()
                        
                #TST{B} dst
                elif(opcode == opcode_c.TST or opcode == opcode_c.TSTB):
                        if(addr_mode == addr_mode_c.reg):
                                operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                eff_addr= find_eff_addr(int(dst), addr_mode, byte_op)
                                operand= read_data(eff_addr, byte_op, 'memory')
                                
                        #Perform 2's complement addition
                        if(byte_op == '1'):
                                result= 0 + int(-operand & 2**8-1)
                        else:
                                result= 0 + int(-operand & 2**16-1)
                                
                        #Don't write back the result
                        
                        #Z: set if the result is 0; cleared otherwise
                        #N: set if the result is < 0; cleared otherwise
                        #C: cleared
                        #V: cleared
                        
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                        
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:17b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                        
                        #C and V cleared for both byte_op and word_op
                        C= '0'
                        V= '0'
                        
                        update_psw()
                        
                #NEG{B} dst
                elif(opcode == opcode_c.NEG or opcode == opcode_c.NEGB):
                        if(addr_mode == addr_mode_c.reg):
                                operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                eff_addr= find_eff_addr(int(dst), addr_mode, byte_op)
                                operand= read_data(eff_addr, byte_op, 'memory')
                                
                        #Perform 2's complement negation
                        if(byte_op == '1'):
                                result= int(-operand & 2**8-1)
                        else:
                                result= int(-operand & 2**16-1)
                        
                        if(addr_mode == addr_mode_c.reg):
                                write_data(int(dst), result, byte_op, 'reg_file')
                        else:
                                write_data(eff_addr, result, byte_op, 'memory')
                        
                        #z: set if the result is 0; cleared otherwise
                        #N: set if the result is < 0; cleared otherwise
                        #c: cleared if the result is 0; set otherwise
                        #v: set if the result is 100000 (word_op); cleared otherwise
                        
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                                if(Z == '1'):
                                        C= '0'
                                else:
                                        C= '1'
                                        
                                if(oct(result) == '0o200'):
                                        V= '1'
                                else:
                                        V= '0'
                        
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:17b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                                if(Z == '1'):
                                        C= '0'
                                else:
                                        C= '1'
                                        
                                if(oct(result) == '0o100000'):
                                        V= '1'
                                else:
                                        V= '0'
                                
                        update_psw()
                        
                #COM{B} dst
                elif(opcode == opcode_c.COM or opcode == opcode_c.COMB):
                        if(addr_mode == addr_mode_c.reg):
                                operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                eff_addr= find_eff_addr(int(dst), addr_mode, byte_op)
                                operand= read_data(eff_addr, byte_op, 'memory')
                                
                        #Take one's complement
                        if(byte_op == '1'):
                                result= int(~operand & 2**8-1)
                        else:
                                result= int(~operand & 2**16-1)
                                
                        if(addr_mode == addr_mode_c.reg):
                                write_data(int(dst), result, byte_op, 'reg_file')
                        else:
                                write_data(eff_addr, result, byte_op, 'memory')
                                
                        #Z: set if result is 0; cleared otherwise
                        #N: set if most significant bit. of result set; cleared otherwise
                        #C: set
                        #V: cleared
                                
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                        
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:17b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                        
                        C= '1'
                        V= '0'
                        
                        update_psw()
                        
                
                #ROR{B} dst
                elif(opcode == opcode_c.ROR or opcode == opcode_c.RORB):
                        if(addr_mode == addr_mode_c.reg):
                                operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                eff_addr= find_eff_addr(int(dst), addr_mode, byte_op)
                                operand= read_data(eff_addr, byte_op, 'memory')
                                
                        if(byte_op == '1'):
                                operand_str= '{0:08b}'.format(operand)
                                C_temp= operand_str[-1]
                                operand= operand >> 1
                                operand_str= '{0:08b}'.format(operand)
                                operand_str= C + operand_str[1:]
                                C= C_temp
                                result= int(operand_str, 2)
                        else:
                                operand_str= '{0:016b}'.format(operand)
                                C_temp= operand_str[-1]
                                operand= operand >> 1
                                operand_str= '{0:016b}'.format(operand)
                                operand_str= C + operand_str[1:]
                                C= C_temp
                                result= int(operand_str, 2)
                                
                        if(addr_mode == addr_mode_c.reg):
                                write_data(int(dst), result, byte_op, 'reg_file')
                        else:
                                write_data(eff_addr, result, byte_op, 'memory')
                                
                        #Z: set if all bits of result = 0; cleared otherwise.
                        #N: set if the high-order bit of the result is set; cleared
                        #otherwise
                        #C: loaded with the low-order bit of the destination
                        #V: loaded with the Exclusive OR of the N-bit and C-bit
                        #(as set by the completion of the rotate operation).
                        
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                        
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:17b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                        #C is calculated above
                        
                        V= str(int(N) ^ int(C))
                        
                        update_psw()
                        
                #ROL{B} dst
                elif(opcode == opcode_c.ROL or opcode == opcode_c.ROLB):
                        if(addr_mode == addr_mode_c.reg):
                                operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                eff_addr= find_eff_addr(int(dst), addr_mode, byte_op)
                                operand= read_data(eff_addr, byte_op, 'memory')
                        
                        if(byte_op == '1'):
                                operand_str= '{0:08b}'.format(operand)
                                C_temp= operand_str[0]
                                operand= operand << 1
                                operand_str= '{0:08b}'.format(operand)
                                operand_str= operand_str[:-1] + C
                                C= C_temp
                                result= int(operand_str, 2)
                        else:
                                operand_str= '{0:016b}'.format(operand)
                                C_temp= operand_str[0]
                                operand= operand << 1
                                operand_str= '{0:016b}'.format(operand)
                                operand_str= operand_str[:-1] + C
                                C= C_temp
                                result= int(operand_str, 2)
                                
                        if(addr_mode == addr_mode_c.reg):
                                write_data(int(dst), result, byte_op, 'reg_file')
                        else:
                                write_data(eff_addr, result, byte_op, 'memory')
                                
                        #Z: set if all bits of the result word = 0; cleared otherwise
                        #N: set if the high-order bit of the result word is set;
                        #cleared otherwise
                        #C: loaded with the high-order bit of the destination
                        #V: loaded with the Exclusive OR of the N-bit and C-bit
                        #(as set by the completion of the rotate operation)
                
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                        
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:17b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                        #C is calculated above
                        
                        V= str(int(N) ^ int(C))
                        
                        update_psw()
                        
                #ASR{B} dst
                elif(opcode == opcode_c.ASR or opcode == opcode_c.ASRB):
                        if(addr_mode == addr_mode_c.reg):
                                operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                eff_addr= find_eff_addr(int(dst), addr_mode, byte_op)
                                operand= read_data(eff_addr, byte_op, 'memory')
                        
                        if(byte_op == '1'):
                                operand_str= '{0:08b}'.format(operand)
                                C= operand_str[-1]
                                C_temp= operand_str[0]
                                operand= operand >> 1
                                operand_str= '{0:08b}'.format(operand)
                                operand_str= C_temp + operand_str[1:]
                                result= int(operand_str, 2)
                        else:
                                operand_str= '{0:016b}'.format(operand)
                                C= operand_str[-1]
                                C_temp= operand_str[0]
                                operand= operand >> 1
                                operand_str= '{0:016b}'.format(operand)
                                operand_str= C_temp + operand_str[1:]
                                result= int(operand_str, 2)
                                
                        if(addr_mode == addr_mode_c.reg):
                                write_data(int(dst), result, byte_op, 'reg_file')
                        else:
                                write_data(eff_addr, result, byte_op, 'memory')
                                
                        #Z: set if the result = 0; cleared otherwise
                        #N: set if the high-order bit of the result is set; cleared
                        #otherwise
                        #C: loaded from the low-order bit of the destination
                        #V: loaded from the Exclusive OR of the N-bit and C-bit
                        #.(as set by the completion,of the shift operation)
                                
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                        
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:17b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                        #C is calculated above
                        
                        V= str(int(N) ^ int(C))
                        
                        update_psw()	
                                
                #ASL{B} dst
                elif(opcode == opcode_c.ASL or opcode == opcode_c.ASLB):
                        if(addr_mode == addr_mode_c.reg):
                                operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                eff_addr= find_eff_addr(int(dst), addr_mode, byte_op)
                                operand= read_data(eff_addr, byte_op, 'memory')	
                        
                        if(addr_mode == addr_mode_c.reg):
                                operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                eff_addr= find_eff_addr(int(dst), addr_mode, byte_op)
                                operand= read_data(eff_addr, byte_op, 'memory')
                                
                        if(byte_op == '1'):
                                operand_str= '{0:08b}'.format(operand)
                                C= operand_str[0]
                                result= operand << 1
                        else:
                                operand_str= '{0:016b}'.format(operand)
                                C= operand_str[0]
                                result= operand << 1
                                
                        if(addr_mode == addr_mode_c.reg):
                                write_data(int(dst), result, byte_op, 'reg_file')
                        else:
                                write_data(eff_addr, result, byte_op, 'memory')
                                
                        #Z: set if the result = 0; cleared otherwise
                        #N: set if the high-order bit of the result is set; cleared
                        #otherwise
                        #C: loaded with the high-order bit of the destination
                        #V: loaded with the Exclusive OR of the N-bit and C-bit
                        #(as set by the completion of the shift operation)
                        
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                        
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:17b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                        #C is calculated above
                        
                        V= str(int(N) ^ int(C))
                        
                        update_psw()
                
                #SWAB dst
                elif(opcode == opcode_c.SWAB):
                        if(addr_mode == addr_mode_c.reg):
                                operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                eff_addr= find_eff_addr(int(dst), addr_mode, byte_op)
                                operand= read_data(eff_addr, byte_op, 'memory')
                                
                        operand_str= '{0:016b}'.format(operand)
                        result= operand_str[8:] + operand_str[:8]
                        result= int(result, 2)
                        
                        if(addr_mode == addr_mode_c.reg):
                                write_data(int(dst), result, byte_op, 'reg_file')
                        else:
                                write_data(eff_addr, result, byte_op, 'memory')
                        
                        #Z: set if low-order byte of result=0; cleared otherwise
                        #N: set if high-order bit of low-order byte (bit 7) of result
                        #is set: cleared otherwise
                        #C: cleared
                        #V: cleared
                        
                        if(int('{0:016b}'.format(result)[8:]) == 0):
                                Z= '1'
                        else:
                                Z= '0'
                        
                        if('{0:016b}'.format(result)[8] == '1'):
                                N= '1'
                        else:
                                N= '0'
                        
                        C= '0'
                        V= '0'
                        
                        update_psw()
                        
        #Two operand instructions. opcode= IR[15:12], src= IR[11:6], dst= IR[5:0]
        elif(instruction_type == "two_operand"):
                #Select opcode bits
                opcode= '{0:06o}'.format(IR)[0:2]
        
                #Select source addressing mode bits
                src_addr_mode= '{0:06o}'.format(IR)[2]
                
                #Select source bits
                src= '{0:06o}'.format(IR)[3]
        
                #Select destination addressing mode bits
                dst_addr_mode= '{0:06o}'.format(IR)[4]
                
                #Select destination bits
                dst= '{0:06o}'.format(IR)[5]
                
                #Check if byte operation
                byte_op= '{0:06o}'.format(IR)[0]
                
                #MOV{B} src, dst
                if(opcode == opcode_c.MOV or opcode == opcode_c.MOVB):
                        #Get src operand
                        if(src_addr_mode == addr_mode_c.reg):
                                src_operand= read_data(int(src), byte_op, 'reg_file')
                        else:
                                src_eff_addr= find_eff_addr(int(src), src_addr_mode, byte_op)
                                src_operand= read_data(src_eff_addr, byte_op, 'memory')
                        
                        #Move src to dst 
                        if(dst_addr_mode == addr_mode_c.reg):
                                if(byte_op == '1'):
                                        #Perform sign extension for operand and then store in dst
                                        src_operand_str= '{0:08b}'.format(src_operand)
                                        sign_src_operand= int((src_operand_str[0]*8 + src_operand_str), 2)
                                        write_data(int(dst), sign_src_operand, 0, 'reg_file')
                                else:
                                        write_data(int(dst), src_operand, byte_op, 'reg_file')
                        else:
                                dst_eff_addr= find_eff_addr(int(dst), dst_addr_mode, byte_op)
                                write_data(dst_eff_addr, src_operand, byte_op, 'memory')        
                        #Z: set if (src) = 0; cleared otherwise
                        #N: set if (src) < 0; cleared otherwise
                        #C: not affected
                        #V: cleared
                        
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(src_operand)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(src_operand)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                        
                        else:
                                if(int('{0:017b}'.format(src_operand)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:17b}'.format(src_operand)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                        #C is not affected
                        
                        V= '0'
                        
                        update_psw()
                
                #ADD src, dst
                elif(opcode == opcode_c.ADD):
                        #Get src operand
                        if(src_addr_mode == addr_mode_c.reg):
                                src_operand= read_data(int(src), byte_op, 'reg_file')
                        else:
                                src_eff_addr= find_eff_addr(int(src), src_addr_mode, byte_op)
                                src_operand= read_data(src_eff_addr, byte_op, 'memory')
                                
                        #Get dst operand
                        if(dst_addr_mode == addr_mode_c.reg):
                                dst_operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                dst_eff_addr= find_eff_addr(int(dst), dst_addr_mode, byte_op)
                                dst_operand= read_data(dst_eff_addr, byte_op, 'memory')
                                
                        result= src_operand + dst_operand
                        
                        #Write result to dst
                        if(dst_addr_mode == addr_mode_c.reg):
                                write_data(int(dst), result, byte_op, 'reg_file')
                        else:
                                write_data(dst_eff_addr, result, byte_op, 'memory')
                                
                        #Z: set if result = 0; cleared otherwise
                        #N: set if result < 0; cleared otherwise
                        #C: set if there was a carry from the most significant bit
                        #of the result; cleared otherwise
                        #V: set if there was arithmetic overflow as a result of the
                        #operation, that is, if both dperands were of the same
                        #sign and the result was of the opposite sign; cleared
                        #otherwise
                                
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                                if('{0:09b}'.format(result)[0] == '1'):
                                        C= '1'
                                else:
                                        C= '0'
                                        
                                src_operand_str= '{0:09b}'.format(src_operand)
                                dst_operand_str= '{0:09b}'.format(dst_operand)
                                result_str= '{0:09b}'.format(result)
                                
                                if((src_operand_str[1] == '0' and dst_operand_str[1] == '0' and result_str[1] == '1') or (src_operand_str[1] == '1' and dst_operand_str[1] == '1' and result_str[1] == '0')):
                                        V= '1'
                                else:
                                        V= '0'
                        
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:17b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                        
                                if('{0:017b}'.format(result)[0] == '1'):
                                        C= '1'
                                else:
                                        C= '0'
                        
                                src_operand_str= '{0:017b}'.format(src_operand)
                                dst_operand_str= '{0:017b}'.format(dst_operand)
                                result_str= '{0:017b}'.format(result)
                                
                                if((src_operand_str[1] == '0' and dst_operand_str[1] == '0' and result_str[1] == '1') or (src_operand_str[1] == '1' and dst_operand_str[1] == '1' and result_str[1] == '0')):
                                        V= '1'
                                else:
                                        V= '0'
                                
                        update_psw()
                
                #SUB src, dst
                elif(opcode == opcode_c.SUB):
                        byte_op = "0"
                        #Get src operand
                        if(src_addr_mode == addr_mode_c.reg):
                                src_operand= read_data(int(src), byte_op, 'reg_file')
                        else:
                                src_eff_addr= find_eff_addr(int(src), src_addr_mode, byte_op)
                                src_operand= read_data(src_eff_addr, byte_op, 'memory')
                                
                        #Get dst operand
                        if(dst_addr_mode == addr_mode_c.reg):
                                dst_operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                dst_eff_addr= find_eff_addr(int(dst), dst_addr_mode, byte_op)
                                dst_operand= read_data(dst_eff_addr, byte_op, 'memory')
                        
                        if(byte_op == '1'):
                                result= dst_operand + int(-src_operand & 2**8-1)
                        else:
                                result= dst_operand + int(-src_operand & 2**16-1)
                        
                        #Write result to dst
                        if(dst_addr_mode == addr_mode_c.reg):
                                write_data(int(dst), result, byte_op, 'reg_file')
                        else:
                                write_data(dst_eff_addr, result, byte_op, 'memory')
                                
                        #N: set if result < 0; cleared otherwise
                        #C: cleared if there was a carry from the most significant
                        #bit of the result: set otherwise
                        #V: set if there was arithmetic overflow as a result of the
                        #operation, that is, if the operands were of opposite
                        #signs and the sign of source was the Same as the
                        #sign of the result; cleared otherwise.
                                
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                                if('{0:09b}'.format(result)[0] == '1'):
                                        C= '0'
                                else:
                                        C= '1'
                                        
                                src_operand_str= '{0:09b}'.format(src_operand)
                                dst_operand_str= '{0:09b}'.format(dst_operand)
                                result_str= '{0:09b}'.format(result)
                                
                                if((src_operand_str[1] == '0' and dst_operand_str[1] == '1' and result_str[1] == '0') or (src_operand_str[1] == '1' and dst_operand_str[1] == '0' and result_str[1] == '1')):
                                        V= '1'
                                else:
                                        V= '0'
                        
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:17b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                        
                                if('{0:017b}'.format(result)[0] == '1'):
                                        C= '0'
                                else:
                                        C= '1'
                        
                                src_operand_str= '{0:017b}'.format(src_operand)
                                dst_operand_str= '{0:017b}'.format(dst_operand)
                                result_str= '{0:017b}'.format(result)
                                
                                if((src_operand_str[1] == '0' and dst_operand_str[1] == '1' and result_str[1] == '0') or (src_operand_str[1] == '1' and dst_operand_str[1] == '0' and result_str[1] == '1')):
                                        V= '1'
                                else:
                                        V= '0'
                                
                        update_psw()	
                                
                #CMP{B} src, dst
                elif(opcode == opcode_c.CMP or opcode == opcode_c.CMPB):
                        #Get src operand
                        if(src_addr_mode == addr_mode_c.reg):
                                src_operand= read_data(int(src), byte_op, 'reg_file')
                        else:
                                src_eff_addr= find_eff_addr(int(src), src_addr_mode, byte_op)
                                src_operand= read_data(src_eff_addr, byte_op, 'memory')
                                
                        #Get dst operand
                        if(dst_addr_mode == addr_mode_c.reg):
                                dst_operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                dst_eff_addr= find_eff_addr(int(dst), dst_addr_mode, byte_op)
                                dst_operand= read_data(dst_eff_addr, byte_op, 'memory')
                                
                        if(byte_op == '1'):
                                result= src_operand + int(-dst_operand & 2**8-1)
                        else:
                                result= src_operand + int(-dst_operand & 2**16-1)
                                
                        #No write back. Doesn't affect either operands. Only updates flags
                                
                        #Z: set if result = 0; cleared otherwise
                        #N: set if result < 0; cleared ptherwise
                        #C: cleared if there was a carry from the most significant
                        #bit of the result; set otherwise
                        #V: set if there was arithmetic overflow; that is, operands
                        #were of opposite signs and the sign of the destination
                        #was the same as the sign of the result; cleared
                        #otherwise
                                
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                                if('{0:09b}'.format(result)[0] == '1'):
                                        C= '0'
                                else:
                                        C= '1'
                                        
                                src_operand_str= '{0:09b}'.format(src_operand)
                                dst_operand_str= '{0:09b}'.format(dst_operand)
                                result_str= '{0:09b}'.format(result)
                                
                                if((src_operand_str[1] == '0' and dst_operand_str[1] == '1' and result_str[1] == '1') or (src_operand_str[1] == '1' and dst_operand_str[1] == '0' and result_str[1] == '0')):
                                        V= '1'
                                else:
                                        V= '0'
                        
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:17b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                        
                                if('{0:017b}'.format(result)[0] == '1'):
                                        C= '0'
                                else:
                                        C= '1'
                        
                                src_operand_str= '{0:017b}'.format(src_operand)
                                dst_operand_str= '{0:017b}'.format(dst_operand)
                                result_str= '{0:017b}'.format(result)
                                
                                if((src_operand_str[1] == '0' and dst_operand_str[1] == '1' and result_str[1] == '1') or (src_operand_str[1] == '1' and dst_operand_str[1] == '0' and result_str[1] == '0')):
                                        V= '1'
                                else:
                                        V= '0'
                        update_psw()	
                
                #BIS{B} src, dst
                elif(opcode == opcode_c.BIS or opcode == opcode_c.BISB):
                        #Get src operand
                        if(src_addr_mode == addr_mode_c.reg):
                                src_operand= read_data(int(src), byte_op, 'reg_file')
                        else:
                                src_eff_addr= find_eff_addr(int(src), src_addr_mode, byte_op)
                                src_operand= read_data(src_eff_addr, byte_op, 'memory')
                                
                        #Get dst operand
                        if(dst_addr_mode == addr_mode_c.reg):
                                dst_operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                dst_eff_addr= find_eff_addr(int(dst), dst_addr_mode, byte_op)
                                dst_operand= read_data(dst_eff_addr, byte_op, 'memory')
                                
                        result= src_operand | dst_operand
                        
                        #Write result to dst
                        if(dst_addr_mode == addr_mode_c.reg):
                                write_data(int(dst), result, byte_op, 'reg_file')
                        else:
                                write_data(dst_eff_addr, result, byte_op, 'memory')
                                
                        #Z: set if result = 0; cleared otherwise
                        #N: set if high-order bit of result set; cleared otherwise
                        #C: not affected
                        #V: cleared
                        
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                        
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:17b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                        #C not affected
                        
                        V= '0'
                        
                        update_psw()
                        
                #BIC{B} src, dst
                elif(opcode == opcode_c.BIC or opcode == opcode_c.BICB):
                        #Get src operand
                        if(src_addr_mode == addr_mode_c.reg):
                                src_operand= read_data(int(src), byte_op, 'reg_file')
                        else:
                                src_eff_addr= find_eff_addr(int(src), src_addr_mode, byte_op)
                                src_operand= read_data(src_eff_addr, byte_op, 'memory')
                                
                        #Get dst operand
                        if(dst_addr_mode == addr_mode_c.reg):
                                dst_operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                dst_eff_addr= find_eff_addr(int(dst), dst_addr_mode, byte_op)
                                dst_operand= read_data(dst_eff_addr, byte_op, 'memory')
                                
                        if(byte_op == '1'):			
                                result= int(~src_operand & 2**8-1) & dst_operand
                        else:
                                result= int(~src_operand & 2**16-1) & dst_operand
                        
                        #Write result to dst
                        if(dst_addr_mode == addr_mode_c.reg):
                                write_data(int(dst), result, byte_op, 'reg_file')
                        else:
                                write_data(dst_eff_addr, result, byte_op, 'memory')
                                
                        #Z: set if result = 0; cleared otherwise
                        #N: set if high-order bit of result set; cleared otherwise
                        #C: not affected
                        #V: cleared
                        
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                        
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:17b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                        #C not affected
                        
                        V= '0'
                        
                        update_psw()
                        
                #BIT{B} src, dst
                elif(opcode == opcode_c.BIT or opcode == opcode_c.BITB):
                        #Get src operand
                        if(src_addr_mode == addr_mode_c.reg):
                                src_operand= read_data(int(src), byte_op, 'reg_file')
                        else:
                                src_eff_addr= find_eff_addr(int(src), src_addr_mode, byte_op)
                                src_operand= read_data(src_eff_addr, byte_op, 'memory')
                                
                        #Get dst operand
                        if(dst_addr_mode == addr_mode_c.reg):
                                dst_operand= read_data(int(dst), byte_op, 'reg_file')
                        else:
                                dst_eff_addr= find_eff_addr(int(dst), dst_addr_mode, byte_op)
                                dst_operand= read_data(dst_eff_addr, byte_op, 'memory')
                
                        result= src_operand & dst_operand
                        
                        #No result write back. Only updates condition codes.
                        
                        #Z: set if result = 0; cleared otherwise
                        #N: set if high-order bit of result set; cleared otherwise
                        #C: not affected
                        #V: cleared
                        
                        if(byte_op == '1'):
                                if(int('{0:09b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:09b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                        
                        else:
                                if(int('{0:017b}'.format(result)[1:]) == 0):
                                        Z= '1'
                                else:
                                        Z= '0'
                                
                                if('{0:17b}'.format(result)[1] == '1'):
                                        N= '1'
                                else:
                                        N= '0'
                                        
                        #C not affected
                        
                        V= '0'
                        
                        update_psw()
                        
        #Zero operand instructions. opcode= IR[15:0]
        if(instruction_type == "zero_operand"):
                #Select opcode bits
                opcode= '{0:06o}'.format(IR)
                
                #CLC/SEC
                if(opcode == opcode_c.CLC or opcode == opcode_c.SEC):
                        if(opcode == opcode_c.CLC):
                                C= '0'
                        else:
                                C= '1'
                        update_psw()
                        
                #CLV/SEV
                elif(opcode == opcode_c.CLV or opcode == opcode_c.SEV):
                        if(opcode == opcode_c.CLV):
                                V= '0'
                        else:
                                V= '1'
                        update_psw()
                        
                #CLZ/SEZ
                elif(opcode == opcode_c.CLZ or opcode == opcode_c.SEZ):
                        if(opcode == opcode_c.CLZ):
                                Z= '0'
                        else:
                                Z= '1'
                        update_psw()
                        
                #CLN/SEN
                elif(opcode == opcode_c.CLN or opcode == opcode_c.SEN):
                        if(opcode == opcode_c.CLN):
                                N= '0'
                        else:
                                N= '1'
                        update_psw()
                        
        #Branch instructions. opcode= IR[15:8], offset= IR[8:0]
        elif(instruction_type == "branch"):
                #Select opcode bits
                #opcode= '{0:2h}'.format(IR)[0:8]
                opcode = '{0:04x}'.format(IR)[0:2]
                
                #Select offset bits
                offset= '{0:16b}'.format(IR)[8:]

                # NZVC conversion to integers
                N_int = int(N, 2)
                Z_int = int(Z, 2)
                C_int = int(C, 2)
                V_int = int(V, 2) 

        #calculating offset
                #New PC address = updated PC + (2 x offset)
                #updated PC = address of branch instruction + 2
                
                #2's complement of offset magnitude if sign bit is 1
                if(offset[0] == '1'):
                        offset_mag= -1 * int(-int(offset[1:],2) & 2**7-1)
                else:
                        offset_mag= int(offset[1:],2)
                
        #converting offset octal string into integer
                offset_int = int(offset[1:],8)

        #read PC as int type
                PC = read_data(reg_file_c.pc,"0","reg_file")

        #calculate new PC as int type
                PC_new = PC + (2 * offset_mag)
                
                #BR offset
                if(opcode == opcode_c.BR):
                        write_data(reg_file_c.pc, PC_new,"0", 'reg_file')
                        branch_record(PC - 2, "BR", PC_new, 1)
                
                #BNE offset
                elif(opcode == opcode_c.BNE):
                        if(Z_int == 0):
                                write_data(reg_file_c.pc,PC_new,"0", 'reg_file')
                                branch_record(PC - 2, "BNE", PC_new, 1)
                        else:
                                branch_record(PC - 2, "BNE", PC, 0)
                
                #BEQ offset
                elif(opcode == opcode_c.BEQ):
                        if(Z_int == 1):
                                write_data(reg_file_c.pc,PC_new,"0", 'reg_file')
                                branch_record(PC-2, "BEQ", PC_new, 1)
                        else:
                                branch_record(PC-2, "BEQ", PC, 0)
                
                #BPL offset
                elif(opcode == opcode_c.BPL):
                        if(N_int == 0):
                                write_data(reg_file_c.pc,PC_new,"0", 'reg_file')
                                branch_record(PC-2, "BPL", PC_new, 1)
                        else:
                                branch_record(PC-2, "BPL", PC, 0)
                                
                #BMI offset
                elif(opcode == opcode_c.BMI):
                        if(N_int == 1):
                                write_data(reg_file_c.pc,PC_new,"0", 'reg_file')
                                branch_record(PC-2, "BMI", PC_new, 1)
                        else:
                                branch_record(PC-2, "BMI", PC, 0)
                
                #BVC offset
                elif(opcode == opcode_c.BVC):
                        if(V_int == 0):
                                write_data(reg_file_c.pc,PC_new,"0", 'reg_file')
                                branch_record(PC-2, "BVC", PC_new, 1)
                        else:
                                branch_record(PC-2, "BVC", PC, 0)
                
                #BVS offset
                elif(opcode == opcode_c.BVS):
                        if(V_int == 1):
                                write_data(reg_file_c.pc,PC_new,"0", 'reg_file')
                                branch_record(PC-2, "BVS", PC_new, 1)
                        else:
                                branch_record(PC-2, "BVS", PC, 0)
                
                #BHIS offset
                elif(opcode == opcode_c.BHIS):
                        if(C_int == 0):
                                write_data(reg_file_c.pc,PC_new,"0", 'reg_file')
                                branch_record(PC-2, "BHIS", PC_new, 1)
                        else:
                                branch_record(PC-2, "BHIS", PC, 0)
                #BCC offset
                elif(opcode == opcode_c.BCC):
                        if(C_int == 0):
                                write_data(reg_file_c.pc,PC_new,"0", 'reg_file')
                                branch_record(PC-2, "BCC", PC_new, 1)
                        else:
                                branch_record(PC-2, "BCC", PC, 0)
                
                #BLO offset
                elif(opcode == opcode_c.BLO):
                        if(C_int == 1):
                                write_data(reg_file_c.pc,PC_new,"0", 'reg_file')
                                branch_record(PC-2, "BLO", PC_new, 1)
                        else:
                                branch_record(PC-2, "BLO", PC, 0)
                                
                #BCS offset
                elif(opcode == opcode_c.BCS):
                        if(C_int == 1):
                                write_data(reg_file_c.pc,PC_new,"0", 'reg_file')
                                branch_record(PC-2, "BCS", PC_new, 1)
                        else:
                                branch_record(PC-2, "BCS", PC, 0)
                
                #BGE offset
                elif(opcode == opcode_c.BGE):
                        if(N_int^V_int == 0):
                                write_data(reg_file_c.pc,PC_new,"0", 'reg_file')
                                branch_record(PC-2, "BGE", PC_new, 1)
                        else:
                                branch_record(PC-2, "BGE", PC, 0)
                
                #BLT offset
                elif(opcode == opcode_c.BLT):
                        if(N_int^V_int == 1):
                                write_data(reg_file_c.pc,PC_new,"0", 'reg_file')
                                branch_record(PC-2, "BLT", PC_new, 1)
                        else:
                                branch_record(PC-2, "BLT", PC, 0)
                
                #BGT offset
                elif(opcode == opcode_c.BGT):
                        if((Z_int|(N_int^V_int)) == 0):
                                write_data(reg_file_c.pc,PC_new,"0", 'reg_file')
                                branch_record(PC-2, "BGT", PC_new, 1)
                        else:
                                branch_record(PC-2, "BGT", PC, 0)
                                
                #BLE offset
                elif(opcode == opcode_c.BLE):
                        if((Z_int|(N_int^V_int)) == 1):
                                write_data(reg_file_c.pc,PC_new,"0", 'reg_file')
                                branch_record(PC-2, "BLE", PC_new, 1)
                        else:
                                branch_record(PC-2, "BLE", PC, 0)
                                
                #BHI offset
                elif(opcode == opcode_c.BHI):
                        if((C_int|Z_int) == 0):
                                write_data(reg_file_c.pc,PC_new,"0", 'reg_file')
                                branch_record(PC-2, "BHI", PC_new, 1)
                        else:
                                branch_record(PC-2, "BHI", PC, 0)
                                
                #BLOS offset
                elif(opcode == opcode_c.BLOS):
                        if((C_int|Z_int) == 1):
                                write_data(reg_file_c.pc,PC_new,"0", 'reg_file')
                                branch_record(PC-2, "BLOS", PC_new, 1)
                        else:
                                branch_record(PC-2, "BLOS", PC, 0)
                                
        #Jump instructions. opcode= IR[15:6], dst= IR[5:0]
        elif(instruction_type == "JMP"):
                #Select opcode bits
                opcode= '{0:06o}'.format(IR)[0:4]
        
                #Select addressing mode bits
                addr_mode= '{0:06o}'.format(IR)[4]
        
                #Select destination bits
                dst= '{0:06o}'.format(IR)[5]

                PC = int(read_reg(7), 8)
                
                if(opcode == opcode_c.JMP):                
                        if(addr_mode == addr_mode_c.reg):
                                eff_addr = read_data(int(dst), '0', 'reg_file')
                                write_data(reg_file_c.pc, eff_addr, "0", 'reg_file')
                        else:
                                eff_addr = find_eff_addr(int(dst), addr_mode, '0')
                                write_data(reg_file_c.pc,eff_addr,"0", 'reg_file')

                #Record the branch trace
                branch_record(PC-2, "JMP", eff_addr, 1)

                '''
                        eff_addr= find_eff_addr(int(dst), addr_mode, '0')
                        write_data(reg_file_c.pc,eff_addr,"0", 'reg_file')	
                '''
                
        #Subroutine instruction. opcode= IR[15:9], reg= IR[8:6], dst= IR[5:0]
        elif(instruction_type == "JSR"):
                #Select opcode bits
                
                opcode= '{0:06o}'.format(IR)[0:3]
                
                # Source register doesn't have any mode
                # The data is directly accessed from the register
                
                # Select source register
                src= '{0:06o}'.format(IR)[3]
                
                # Source operand 
                src_operand = read_data(int(src), '0', 'reg_file')
                
                # Select destination addressing mode bits
                dst_addr_mode= '{0:06o}'.format(IR)[4]
                
                # Select destination register
                dst = '{0:06o}'.format(IR)[5]

                #Current PC value 
                PC = int(read_reg(7), 8)
                
                if(dst_addr_mode == addr_mode_c.reg):
                        dst_operand = read_data(int(dst), '0', 'reg_file')
                else:
                        eff_addr = find_eff_addr(int(dst), dst_addr_mode, '0')
                        dst_operand = read_data(eff_addr, '0', 'memory')
                
                # Pseudo code
                # dst -> (tmp)
                # push specified reg(src)
                # (PC) -> (reg)
                # (tmp) -> (PC)
                
                # Storing the dst_operand (JUMP address) in a temporary register
                temp = dst_operand
                
                # Pushing the specified register to the stack
                sp_address = read_data(reg_file_c.sp, '0', 'reg_file')
                sp_address = sp_address - 2
                write_data(reg_file_c.sp, sp_address, "0", 'reg_file')
                write_data(sp_address, src_operand, "0", 'memory')
                
                # Moving the current PC to the register
                PC_address = read_data(reg_file_c.pc, '0', 'reg_file')
                write_data(int(src), PC_address, '0', 'reg_file')
                
                # Moving the temporary to the PC
                write_data(reg_file_c.pc, eff_addr, '0', 'reg_file')

                #Record the branch trace
                branch_record(PC-2, "JSR", dst_operand, 1)
                
        #Return from subroutine
        elif(instruction_type == "RTS"):
        
                # Select destination register
                dst = '{0:06o}'.format(IR)[5]
                dst_operand = read_data(int(dst), '0', 'reg_file')
                
                #Pseudo code 
                # (reg) -> (PC) 
                # Pop stack -> (reg) 
                
                # Move reg data to the PC
                PC = int(read_reg(7), 8)
                write_data(reg_file_c.pc, dst_operand, '0', 'reg_file')
                
                # Pop stack and store it in reg
                sp_address = read_data(reg_file_c.sp, '0', 'reg_file')
                saved_reg = read_data(sp_address, '0', 'memory')
                write_data(int(dst), saved_reg, '0', 'reg_file')

                # Record the branch trace
                branch_record(PC-2, "RTS", dst_operand, 1)
                
