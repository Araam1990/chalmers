start:
	LDR	R0,=intvec
	LDR	R1,=shortvec
	MOV	R2,#8
	BL	copyvec
	B	start
copyvec:
	PUSH	{LR}
	MOV	R3,#0
copyvec_1:
	CMP	R3,R2
	BGE	copyvec_2
	LSL	R5,R3,#1
	LDRSH	R4,[R1,R5]
	LSL	R5,R3,#2
	STR	R4,[R0,R5]
	ADD	R3,R3,#1
	B	copyvec_1
copyvec_2:
	POP	{PC}
	BX	LR

	.ORG	0x30
intvec:	
	.SPACE	32
shortvec:
	.HWORD	1,2,3,4,-1,-2,-3,-4
