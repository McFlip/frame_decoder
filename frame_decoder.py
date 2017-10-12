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
    print "frame ", num, ", size ", len(frame), ": invalid  **frame too small***"
  else:
    checksum = frame[-2:]
    #print "checkbits: ", binascii.hexlify(checksum)
    #print "type of checkbits: ", type(binascii.hexlify(checksum))
    payload = frame[0:-2]
    #if validate(payload, Bits(bytes=checksum).bin[2:]):
    #if validate(payload, ''.join([bin(c)[2:] for c in checksum])):
    if validate(payload, binascii.hexlify(checksum)):
      msg.append(str(payload))
      print "frame ", num, ", size ", len(frame), ": valid"
    else:
      print "frame ", num, ", size ", len(frame), ": invalid"
    del frame[:]

def validate(p, cs):
  twobit = scramble(p)
  if calcCheckSum(twobit.bin, cs) == 0:
    return True
  else:
    return False

def scramble(ordered):
  sbits = BitArray()
  #print "FUBAR: ", ordered
  for byte in ordered:
    #print "ordered: ", byte
    b = Bits(uint=byte, length=8)
    #print "ordered: ", b.bin
    sbits.append(BitArray(bool=b[0]))
    sbits.append(BitArray(bool=b[4]))
    sbits.append(BitArray(bool=b[1]))
    sbits.append(BitArray(bool=b[5]))
    sbits.append(BitArray(bool=b[2]))
    sbits.append(BitArray(bool=b[6]))
    sbits.append(BitArray(bool=b[3]))
    sbits.append(BitArray(bool=b[7]))

    #print "scramble: ", sbits.bin
  return sbits

def calcCheckSum(input_bitstring, checksum):
  #print "***CHECKSUM FUNCTION"
  #print "input_bitstring: ", input_bitstring
  #print "checksum: ", "0x%x" % (int(checksum, 16))
  #print "checksum: ", "{0:b}".format(int(checksum, 16))
  checksum = "{0:b}".format(int(checksum, 16))
  len_input = len(input_bitstring)
  input_padded_array = list(input_bitstring + checksum.zfill(16))
  #print "input_padded_array: ", input_padded_array
  j = 0
  while '1' in input_padded_array[:len_input]:
    cur_shift = input_padded_array.index('1')
    j += 1
    print j
    for i in range(len(polynomial_bitstring)):
      if polynomial_bitstring[i] == input_padded_array[cur_shift + i]:
        input_padded_array[cur_shift + i] = '0'
      else:
        input_padded_array[cur_shift + i] = '1'
  result = ''.join(input_padded_array)[len_input:]
  #print "crc result: ", result
  return int(result, 2)

# set up arguments
parser = argparse.ArgumentParser(prog='frame_decoder', description='Parses a dump file and extracts the frames.')
parser.add_argument("-i","--infile", help="encoded file", default="output")
parser.add_argument("-o","--outfile", help="decoded file", default=os.path.join(os.getcwd(), "decoded_output"))
args = parser.parse_args()

# check arguments
infile = os.path.expanduser(args.infile)
if not os.path.exists(infile):
  parser.error('The encoded file does not exist!')
if not os.path.isfile(infile):
  parser.error('The encoded file is not a file!')
if not os.access(infile, os.R_OK):
  parser.error('The encoded file is not readable!')

outfile = os.path.basename(os.path.expanduser(args.outfile))
outDir = os.path.dirname(os.path.expanduser(args.outfile))
if not outDir:
  outDir = os.getcwd()
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
global polynomial_bitstring
polynomial_bitstring = '10110000100010011'

# read the file
byte = bytearray(open(infile, 'rb').read())
# check the end and add last flag if needed to prevent problems
if byte[-1] != ord('a'):
  byte.append(ord('a'))

#sentinal = object()

# TESTING
#print byte
#open('short', 'wb').write(byte[0:10])

# Process the dump file
#byte_itr = byte.__iter__()
#for byte_val in byte_itr:
  ##byte_val = byte_itr.next()
  #print "current byte is {:x}".format(byte_val)
  #if byte_val != ord('a'):
    ##if byte_itr != len(byte)-1:
    #byte_val_next = byte_itr.next()
    #while byte_val != ord('a') and byte_val_next != ord('a'):
      ## unstuff; check for escape 'b'
      #if byte_val == ord('b'):
        #byte_val = byte_itr.next()
        #currentFrame.append(byte_val)
        #print "**unstuffed** append byte {:x}".format(byte_val)
        #byte_val = byte_itr.next()
      #else:
        ##currentFrame.append(byte_val)
        #currentFrame.append(byte_val_next)
        #print "append byte {:x}".format(byte_val)
        #byte_val = byte_val_next
        #byte_val_next = byte_itr.next()
    ##end of frame - process frame
    #print binascii.hexlify(currentFrame)
    #decode(currentFrame, frameNum, data)
    ##advance to next
    ##byte_val = byte_itr.next()
    #frameNum += 1
i=0
while i < len(byte):
  #print "i= ", i
  if byte[i] != ord('a'):
    #print "{:x}".format(byte[i]), "cp1"
    i = byte.find(b'a')
    #print "i= ", i
    if i < len(byte) - 1:
      if byte[i+1] != ord('a'):
        #print "{:x}".format(byte[i]), "cp2"
        i = byte.find(b'a')
        #print "i= ", i
  else:
    if i < len(byte)-1:
      if byte[i] == ord('a'):
        while i < len(byte)-1 and byte[i] == ord('a'):
          i += 1
          #print "i= ", i
      while i < len(byte) and byte[i] != ord('a'):
        if byte[i] == ord('b'):
          #print "{:x}".format(byte[i]), "cp3"
          currentFrame.append(byte[i+1])
          i += 2
          #print "i= ", i
        else:
          currentFrame.append(byte[i])
          #print "{:x}".format(byte[i]), "cp4"
          i += 1
          #print "i= ", i
      decode(currentFrame, frameNum, data)
      frameNum += 1
    else:
      i += 1
      #print "i= ", i, "cp5"

print "processed {} frames".format(frameNum)
#print "".join(data)
open(outfile, 'wb').write("".join(data))