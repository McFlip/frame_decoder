#!/usr/bin/python

def crc_remainder(input_bitstring, polynomial_bitstring, initial_filler):
	'''
	Calculates the CRC remainder of a string of bits using a chosen polynomial.
	initial_filler should be '1' or '0'.
	'''
	len_input = len(input_bitstring)
	#initial_padding = initial_filler  * (len(polynomial_bitstring) - 1)
	#input_padded_array = list(input_bitstring + initial_padding)
	input_padded_array = list(input_bitstring + checksum)
	#polynomial_bitstring = polynomial_bitstring.lstrip('0')
	while '1' in input_padded_array[:len_input]:
		cur_shift = input_padded_array.index('1')
		for i in range(len(polynomial_bitstring)):
			if polynomial_bitstring[i] == input_padded_array[cur_shift + i]:
				input_padded_array[cur_shift + i] = '0'
			else:
				input_padded_array[cur_shift + i] = '1'
	return ''.join(input_padded_array)[len_input:]

myinput = '00111001'
generator = '10110000100010011'
filler = '0'
global checksum
checksum = '1001000001100101'

print crc_remainder(myinput, generator, filler)