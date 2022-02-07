start:
	LDR	R0,=0x55555555
	LDR	R1,=0x40020C00
	STR	R0,[R1]

	LDR	R1,=0x40020C14

	LDR	R2,=0x40021010

main:
	LDRH	R0,[R2]
	STRH	R0,[R1]
	B	main

@ H:et i LDRH respektive STRH innebär halfword vilket är vad som inom 
@ assembler representerar 2 Bytes (16 bitar, bit 0-15) medan b:et i 
@ LDRB respektive STRB innebär Byte vilket representerar 1 Byte (8 bitar, 
@ bit 0-7), därav att bit 8-15 endast påverkas av LDRH/STRH