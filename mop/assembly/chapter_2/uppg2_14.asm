start:
	LDR	R0,mptr
	MOV	R1,#32
	MOV	R2,#0xAA
	BL	fillmem
	B	start
fillmem:
.L1:
	CMP	R1,#0
	BEQ	.L2
	STRB	R2,[R0]
	ADD	R0,R0,#1
	SUB	R1,R1,#1
	B	.L1
.L2:
	BX	LR

	.ALIGN
mptr:	.WORD	0x20008000
