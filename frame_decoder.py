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
    payload = frame[0:-2]
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
  for byte in ordered:
    b = Bits(uint=byte, length=8)
    sbits.append(BitArray(bool=b[0]))
    sbits.append(BitArray(bool=b[4]))
    sbits.append(BitArray(bool=b[1]))
    sbits.append(BitArray(bool=b[5]))
    sbits.append(BitArray(bool=b[2]))
    sbits.append(BitArray(bool=b[6]))
    sbits.append(BitArray(bool=b[3]))
    sbits.append(BitArray(bool=b[7]))
  return sbits

def calcCheckSum(input_bitstring, checksum):
  checksum = "{0:b}".format(int(checksum, 16))
  len_input = len(input_bitstring)
  concat_bits = list(input_bitstring + checksum.zfill(16))
  # TESTING j = 0
  while '1' in concat_bits[:len_input]:
    offset = concat_bits.index('1')
    # TESTING += 1
    # TESTING print j
    for i in range(len(generator)):
      if generator[i] == concat_bits[offset + i]:
        concat_bits[offset + i] = '0'
      else:
        concat_bits[offset + i] = '1'
  result = ''.join(concat_bits)[len_input:]
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
global generator
generator = '10110000100010011'

# read the file
byte = bytearray(open(infile, 'rb').read())
# check the end and add last flag if needed to prevent problems
if byte[-1] != ord('a'):
  byte.append(ord('a'))
# parse the byte array
i=0
while i < len(byte):
  if byte[i] != ord('a'):
    i = byte.find(b'a')
    if i < len(byte) - 1:
      if byte[i+1] != ord('a'):
        i = byte.find(b'a')
  else:
    if i < len(byte)-1:
      if byte[i] == ord('a'):
        while i < len(byte)-1 and byte[i] == ord('a'):
          i += 1
      while i < len(byte) and byte[i] != ord('a'):
        if byte[i] == ord('b'):
          currentFrame.append(byte[i+1])
          i += 2
        else:
          currentFrame.append(byte[i])
          i += 1
      decode(currentFrame, frameNum, data)
      frameNum += 1
    else:
      i += 1

# finish
print "processed {} frames".format(frameNum)
open(outfile, 'wb').write("".join(data))