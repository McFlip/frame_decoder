#!/usr/bin/python
# Grady Denton for proj1 in cnt5505 data comm
import argparse
import os
from bitstring import Bits, BitArray
import binascii

# Function definitions
def decode(frame, num, msg):
	checksum = frame[-2:]
	payload = frame[0:-2]
	if validate(payload, checksum):
		msg.append(str(payload))
		print "frame ", num, ", size ", len(payload), ": valid"
	else:
		print "frame ", num, ", size ", len(payload), ": invalid"
	del frame[:]

def validate(p, cs):
	twobit = scramble(p)
	if cs == calcCheckSum(twobit):
		return True
	else:
		return False

def scramble(ordered):
	sbits = BitArray()
	#add for loop cuz arg is bytes
	orderedBits = Bits(ordered)
	#do scramble
	return sbits

def calcCheckSum(i):
	return 1

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