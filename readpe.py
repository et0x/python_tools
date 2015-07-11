#!/usr/bin/python
import os, sys, re, struct, string, binascii, time

fileName = sys.argv[1]
text = open(fileName,"rb").read()
file = open(fileName,"rb")

PTROFFSET= 0x0
PEOFFSET = 0x0
SHOFFSET = 0x0
SCTNNUMS = 0
SSOFFSET = 0x0 	#the offset at which the section headers start (PE+247)
def bytes2int(text,readtype):
	sizeDict = {	"char":"c",
			"uchar":"B",
			"short":"h",
			"ushort":"H",
			"int":"i",
			"uint":"I",
			"ll":"q",
			"ull":"Q"
		    }

	return struct.unpack("<%s"%sizeDict[readtype],text)[0]

	

def printAscii(text):
	return "".join(x for x in text if (x in string.printable))

def txt2hex(text):
	return "0x"+"".join(hex(ord(x))[2:].zfill(2) for x in text)

def int2hex(integer):
	return hex(integer).replace("L","")

def readSectionInfo(sectionHeaderText):
	vsize   = bytes2int(sectionHeaderText[8:12],"uint")
	voffset = bytes2int(sectionHeaderText[12:16],"uint")
	rsize   = bytes2int(sectionHeaderText[16:20],"uint")
	roffset = bytes2int(sectionHeaderText[20:24],"uint")
	flags   = bytes2int(sectionHeaderText[36:40],"uint")
	return vsize,voffset,rsize,roffset,flags

while (1):
	PTROFFSET = file.tell()
	if (( text[PTROFFSET] == "P" ) and (text[PTROFFSET+1] == "E" )):
		print "\n\nFile: %s"%fileName
		print "Found PE header at offset 0x%08x"%PTROFFSET
		PEOFFSET = PTROFFSET
		break
	file.read(1)

file.seek(PEOFFSET+6)
PTROFFSET = file.tell()
CODEBASE = bytes2int(text[PEOFFSET+44:PEOFFSET+48],"uint")
ENTRYPT  = bytes2int(text[PEOFFSET+40:PEOFFSET+44],"uint")
print "codebase is 0x%08x"%CODEBASE
print "Entry Point is: 0x%08x"%ENTRYPT

SHOFFSET = file.tell()
SSOFFSET = PEOFFSET+247

SCTNNUMS = bytes2int(text[PTROFFSET:PTROFFSET+2],"ushort")

print "Found number of sections: %d, "%SCTNNUMS,
print "Offset: 0x%08x"%SHOFFSET

file.seek(PEOFFSET+248) #put the file pointer at the beginning of the section header info
PTROFFSET = file.tell()
headerdict = {}

for section in range(SCTNNUMS):
	d = file.read(40)
	headerdict[section] = d

timestamp = bytes2int(file.read(4),"uint")
sctninfo = 0
i = 0
txtfile = open("rawtxt.bin","wb")
txtsection = ""
for data in headerdict.values():	
	sctninfo = readSectionInfo(data)
	print "Section ['%s']:"%data[:data[:9].find("\x00")]
	print "    VSIZE: 0x%08x"%readSectionInfo(data)[0]
	print "  VOFFSET: 0x%08x"%readSectionInfo(data)[1]
	print "    RSIZE: 0x%08x"%readSectionInfo(data)[2]
	print "  ROFFSET: 0x%08x"%readSectionInfo(data)[3]
	print "    FLAGS: 0x%08x"%readSectionInfo(data)[4]
	if (i == 0):
		txtsection = text[CODEBASE:readSectionInfo(data)[3]+(readSectionInfo(data)[2])]
		txtfile.write(txtsection)
		
		txtfile.close()
	i += 1
print "Date/Timestamp: %s"%time.ctime(timestamp)
