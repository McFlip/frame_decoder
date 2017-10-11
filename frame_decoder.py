#!/usr/bin/python
'''
Grady Denton for proj1 in cnt5505 data comm
'''
import argparse
import os
from bitstring import Bits, BitArray
import binascii

# Function definitions
def decode(frame, num, msg):
  if len(frame) <3:
    print "frame ", num, ", size ", len(payload), ": invalid"
  else:
    checksum = frame[-2:]
    print "checkbits: ", binascii.hexlify(checksum)
    payload = frame[0:-2]
    if validate(payload, Bits(bytes=checksum).bin[2:]):
      msg.append(str(payload))
      print "frame ", num, ", size ", len(payload), ": valid"
    else:
      print "frame ", num, ", size ", len(payload), ": invalid"
    del frame[:]

def validate(p, cs):
  twobit = scramble(p)
  if calcCheckSum(twobit.bin, cs) == 0:
    return True
  else:
    return False

def scramble(ordered):
  sbits = BitArray()
  print "FUBAR: ", ordered
  for byte in ordered:
    print "ordered: ", byte
    b = Bits(uint=byte, length=8)
    print "ordered: ", b.bin
    sbits.append(BitArray(bool=b[0]))
    sbits.append(BitArray(bool=b[4]))
    sbits.append(BitArray(bool=b[1]))
    sbits.append(BitArray(bool=b[5]))
    sbits.append(BitArray(bool=b[2]))
    sbits.append(BitArray(bool=b[6]))
    sbits.append(BitArray(bool=b[3]))
    sbits.append(BitArray(bool=b[7]))

    print "scramble: ", sbits.bin
  return sbits

def calcCheckSum(input_bitstring, checksum):
	len_input = len(input_bitstring)
	input_padded_array = list(input_bitstring + checksum.zfill(16))
	while '1' in input_padded_array[:len_input]:
		cur_shift = input_padded_array.index('1')
		for i in range(len(polynomial_bitstring)):
			if polynomial_bitstring[i] == input_padded_array[cur_shift + i]:
				input_padded_array[cur_shift + i] = '0'
			else:
				input_padded_array[cur_shift + i] = '1'
	return int(''.join(input_padded_array)[len_input:], 2)

# set up arguments
parser = argparse.ArgumentParser(prog='frame_decoder', description='Parses a dump file and extracts the frames.')
parser.add_argument("-i","--infile", help="encoded file", default="output")
parser.add_argument("-o","--outfile", help="decoded file", default=os.path.join(os.getcwd(), "decoded_output"))
args = parser.parse_args()

# check arguments
#infile
infile = os.path.expanduser(args.infile)
if not os.path.exists(infile):
  parser.error('The encoded file does not exist!')
if not os.path.isfile(infile):
  parser.error('The encoded file is not a file!')
if not os.access(infile, os.R_OK):
  parser.error('The encoded file is not readable!')

#outDir
#outfile
outfile = os.path.basename(os.path.expanduser(args.outfile))
outDir = os.path.dirname(os.path.expanduser(args.outfile))
if not os.path.exists(outDir):
    parser.error('The out dir does not exist!')
if not os.path.isdir(outDir):
    parser.error('The out dir is not a directory!')
if not os.access(outDir, os.W_OK):
    parser.error('The outDir dir is not writable!')

# MAIN FUNCTION

# Vars
frameNum = 0
data = []
currentFrame = bytearray()
byte = bytearray(open(infile, 'rb').read())
global polynomial_bitstring
polynomial_bitstring = '10110000100010011'

# TESTING
#print byte
#open('short', 'wb').write(byte[0:10])

# Process the dump file
byte_itr = byte.__iter__()
for byte_val in byte_itr:
  byte_val = byte_itr.next()
  #print "current byte is {:x}".format(byte_val)
  if byte_val != ord('a'):
    while byte_val != ord('a'):
      # unstuff; check for escape 'b'
      if byte_val == ord('b'):
        byte_val = byte_itr.next()
        currentFrame.append(byte_val)
        #print "append byte {:x}".format(byte_val)
        byte_val = byte_itr.next()
      else:
        currentFrame.append(byte_val)
        #print "append byte {:x}".format(byte_val)
        byte_val = byte_itr.next()
    #end of frame - process frame
    print binascii.hexlify(currentFrame)
    decode(currentFrame, frameNum, data)
    #advance to next
    #byte_val = byte_itr.next()
    frameNum += 1
print "processed {} frames".format(frameNum)
print "".join(data)