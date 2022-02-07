start:
	BL	main
	B	start
main:
	PUSH	{LR}
	MOV	R0,#0x10
	PUSH	{R0}
	BL	func
	POP	{R0}
	POP	{PC}
func:
	PUSH	{R7}
	MOV	R7,SP
	LDR	R1,[R7,#4]
	POP	{R7}
	BX	LR
