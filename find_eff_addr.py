#read_data(addr, byte_op, "mem/reg_file")
#write_data(addr, value_to_write, byte_op, "mem/reg_file")

from Classes.classes import opcode_c
from Classes.classes import addr_mode_c
from Classes.classes import reg_file_c

from memory_access import *

#Input arguments are register, addressing mode and byte operation flag
def find_eff_addr(reg, addr_mode, byte_op):

	#Register deferred - OPR (Rn)
	if(addr_mode == addr_mode_c.reg_def):
		eff_addr= read_data(reg, '0', "reg_file")
		return eff_addr

	#Autoincrement - OPR (Rn)+
	elif(addr_mode == addr_mode_c.auto_inc):
		eff_addr_temp= read_data(reg, '0', "reg_file")
		eff_addr= eff_addr_temp;
		
		#If byte operation and not PC, increment addr by 1, else increment by 2
		if(byte_op == '1' and reg != reg_file_c.pc):
			eff_addr_temp += 1
		else:
			eff_addr_temp += 2	
		write_data(reg, eff_addr_temp, '0', "reg_file")
		return eff_addr
	
	#Autoincrement deferred - OPR @(Rn)+
	elif(addr_mode == addr_mode_c.auto_inc_def):
		eff_addr_temp= read_data(reg, '0', "reg_file")
		eff_addr= read_data(eff_addr_temp, '0', "memory")
		
		#Register content pointing to address. So, increment by 2
		eff_addr_temp += 2
		
		write_data(reg, eff_addr_temp, '0', "reg_file")
		return eff_addr
		
	#Autodecrement - OPR (Rn)
	elif(addr_mode == addr_mode_c.auto_dec):
		eff_addr_temp= read_data(reg, '0', "reg_file")
		
		#If byte operation and not PC, decrement addr by 1, else increment by 2
		if(byte_op == '1' and reg != reg_file_c.pc):
			eff_addr_temp -= 1
		else:
			eff_addr_temp -= 2
			
		eff_addr= eff_addr_temp
		write_data(reg, eff_addr_temp, '0', "reg_file")
		return eff_addr
	
	#Autodecrement deferred - OPR @-(Rn)
	elif(addr_mode == addr_mode_c.auto_dec_def):
		eff_addr_temp= read_data(reg, '0', "reg_file")
		
		#Register content pointing to address. So, decrement by 2
		eff_addr_temp -= 2
		
		eff_addr= read_data(eff_addr_temp, '0', "memory")
		write_data(reg, eff_addr_temp, '0', "reg_file")
		return eff_addr
		
	#Index - OPR X(Rn)
	elif(addr_mode == addr_mode_c.index):
		pc= read_data(reg_file_c.pc, '0', "reg_file")
		eff_addr= read_data(pc, '0', "memory")			#Read X
		pc += 2
		write_data(reg_file_c.pc, pc, '0', "reg_file")
		eff_addr_temp= read_data(reg, '0', "reg_file")	#Read (Rn)
		eff_addr= eff_addr + eff_addr_temp	#X + (Rn)
		return eff_addr
	
	#Index deferred - OPR @X(Rn)
	elif(addr_mode == addr_mode_c.index_def):
		pc= read_data(reg_file_c.pc, '0', "reg_file")
		eff_addr= read_data(pc, '0', "memory")
		pc += 2
		write_data(reg_file_c.pc, pc, '0', "reg_file")
		eff_addr_temp= read_data(reg, '0', "reg_file")
		eff_addr= eff_addr + eff_addr_temp
		eff_addr= read_data(eff_addr, '0', "memory")
		return eff_addr

	
