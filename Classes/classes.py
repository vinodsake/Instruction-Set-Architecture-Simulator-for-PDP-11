#class instruction_type_c:
#    zero_operand, one_operand, one_half_operand, two_operand, branch, others = range(6)

class addr_mode_c:
    reg, reg_def, auto_inc, auto_inc_def, auto_dec, auto_dec_def, index, index_def = ('0', '1', '2', '3', '4', '5', '6', '7')

class reg_file_c:
    reg0, reg1, reg2, reg3, reg4, reg5, sp, pc = range(8)

class opcode_c:
	#Zero-operand instructions. 16bit opcode. All values in octal
	HALT= '000000'		#HALT
	#WAIT= '000001'		#WAit for InterrupT
	#RESET= '000005'		#RESet ExTernal bus
	#NOP= '000240'		#Not found in handbook
	#Processor Status Word (PSW) istructions. All values in octal
	#SPL not implemented
	CLC= '000241'		#CLear C
	CLV= '000242'		#CLear V
	CLZ= '000244'		#CLear Z
	CLN= '000250'		#CLear N
	SEC= '000261'		#SEt C
	SEV= '000262'		#SEt V
	SEZ= '000264'		#SEt Z
	SEN= '000270'		#SEt N
	#CCC= '000257'		#Not found in handbook
	#SCC= '000277'		#Not found in handbook
	
	#One-operand instructions. 10bit opcode. All values in octal
	CLR= '0050'			#CLeaR
	CLRB= '1050'		#CLeaR Byte
	INC= '0052'			#INCrement
	INCB= '1052'		#INCrement Byte
	DEC= '0053'			#DECrement
	DECB= '1053'		#DECrement Byte
	ADC= '0055'			#ADd Carry
	ADCB= '1055'		#ADd Carry Byte
	SBC= '0056'			#SuBtract Carry
	SBCB= '1056'		#SuBtract Carry Byte
	TST= '0057'			#TeST
	TSTB= '1057'		#TeST Byte
	NEG= '0054'			#NEGate
	NEGB= '1054'		#NEGate Byte
	COM= '0051'			#COMplement
	COMB= '1051'		#COMplement Byte
	ROR= '0060'			#ROtate Right
	RORB= '1060'		#ROtate Right Byte
	ROL= '0061'			#ROtate Left
	ROLB= '1061'		#ROtate Left Byte
	ASR= '0062'			#Arithmetic Shift Right
	ASRB= '1062'		#Arithmetic Shift Right Byte
	ASL= '0063'			#Arithmetic Shift Left
	ASLB= '1063'		#Arithmetic Shift Left Byte
	SWAB= '0003'		#SWAp Bytes
	SXT= '0067'			#Not found in handbook
	
	#One-and-a-half-operand instructions. 7bit opcode. All values in octal
	#MUL= '070'			#Not found in handbook
	#DIV= '071'			#Not found in handbook
	#ASH= '072'			#Not found in handbook
	#ASHC= '073'			#Not found in handbook
	#XOR= '074'			#Not found in handbook
	
	#Two-operand instructions. 4bit opcode. All values in octal
	MOV= '01'			#MOVe
	MOVB= '11'			#MOVe Byte
	ADD= '06'			#ADD
	SUB= '16'			#SUBtract
	CMP= '02'			#CoMPare
	CMPB= '12'			#CoMPare Byte
	BIS= '05'			#BItSet
	BISB= '15'			#BItSet Byte
	BIC= '04'			#BItClear
	BICB= '14'			#BItClear Byte
	BIT= '03'			#BItTest
	BITB= '13'			#BItTest Byte
	
	#Branch instructions. 8bit opcode. All values in hexadecimal
	BR= '01'			#Branh
	BNE= '02'			#Branch on Not Equal
	BEQ= '03'			#Branch on EQual
	BPL= '80'			#Branch on PLus
	BMI= '81'			#Branch on MInus
	BVC= '84'			#Branch on oVerflow Clear
	BVS= '85'			#Branch on oVerflow Set
	BHIS= '86'			#Branch on HIgher or Same
	BCC= '86'  			#Branch on Carry Clear
	BLO= '87'			#Branch on LOwer
	BCS= '87'			#Branch on Carry Set
	BGE= '04'			#Branch on Greater than or Equal
	BLT= '05'			#Branch on Less Than
	BGT= '06'			#Branch on Greater Than
	BLE= '07'			#Branch on Less than or Equal
	BHI= '82'			#Branch on HIgher
	BLOS= '83'			#Branch on LOwer or Same
	
	#Other instrucions involving transfer of control. All values in octal
	#RTI, TRAP, BPT, IOT, EMT, RTT not implemented
	JMP= '0001'			#JuMP
	#SOB= '077'			#Not found in handbook
	JSR= '004'			#Jump to SubRoutine
	RTS= '00020'		#ReTurn from Subroutine
