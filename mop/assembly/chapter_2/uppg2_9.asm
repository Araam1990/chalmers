start:
	LDR	R0,=0x55555555
	LDR	R1,=0x40020C00
	STR	R0,[R1]
	LDR	R5,=0x40020C14
	LDR	R6,=0x40021010
main:
	LDRB	R0,[R6]
	LDRB	R1,[R6,#1]
	CMP	R0,R1
	BHI	main_1
	@BGT	main_1
	MOV	R0,#0
	B	main_2
main_1:
	MOV	R0,#0xFF
main_2:
	STRB	R0,[R5]
	B	main
