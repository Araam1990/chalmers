start:	mov 	r0, #89
	mov 	r1, #166
	mov 	r2, #133
	sbc 	r2, r2, r1
	add 	r2, r2, r1
	orr 	r0, r0, r2
	mul 	r2, r2, r1
	adc 	r1, r1, r0
	sub 	r0, r0, r1
	orr 	r0, r0, r2
	adc 	r1, r1, r0
	sbc 	r0, r0, r1
	sub 	r0, r0, r0
	eor 	r0, r0
	eor 	r0, r1
	eor 	r0, r2
	ldr 	r1, =0x000000FF
	and 	r0, r1
end: 	b 	end
