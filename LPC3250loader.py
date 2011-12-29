#!/usr/bin/env python

import sys, os, serial, threading

loadaddr = 0x00000000
imgaddr = 0x80000004

serialport = "/dev/ttyUSB0"
burnerfile = "/home/alex/burner.bin"
imagefile = "/home/alex/kick.bin"

ser = serial.Serial(serialport, 115200, timeout=300)

print "Waiting for BOOTID..."

while True:
    input = ser.read()
    print "%d %c" % (ord(input), input)
    if input == '5':
        break

print "OK"
ser.write('A')
input = 0


print "Waiting for 2nd BOOTID..."

input = ser.read()
print "%d %c" % (ord(input), input)
if input != '5':
    print "error 2"
    sys.exit()

print "OK"
ser.write('U3')
input = 0

print "Waiting for 2nd BOOTID..."

input = ser.read()
print "%d %c" % (ord(input), input)
if input != 'R':
    print "error 3"
    sys.exit()

print "Loadaddress: %d" % (loadaddr)
val = loadaddr
for i in range(4):
    ser.write(chr(val&0xFF))
    val = val >> 8

size = os.path.getsize(burnerfile)
print "Filesize: %d" % (size)
val = size
for i in range(4):
    ser.write(chr(val&0xFF))
    val = val >> 8


f = open(burnerfile, "rb")
try:
    byte = f.read(1)
    while byte != "":
        ser.write(byte)
        byte = f.read(1)
finally:
    f.close()

input = ser.read()
print "%d %c" % (ord(input), input)
if input != 'X':
    print "error 4"
    sys.exit()

ser.write('p')

print "Image address: %d" % (imgaddr)
val = imgaddr
for i in range(4):
    ser.write(chr(val&0xFF))
    val = val >> 8

size = os.path.getsize(imagefile)
print "Filesize: %d" % (size)
val = size
for i in range(4):
    ser.write(chr(val&0xFF))
    val = val >> 8

input = ser.read()
print "%d %c" % (ord(input), input)
if input != 'o':
    print "error 5"
    sys.exit()

f = open(imagefile, "rb")
try:
    byte = f.read(1)
    while byte != "":
        ser.write(byte)
        byte = f.read(1)
finally:
    f.close()

input = ser.read()
print "%d %c" % (ord(input), input)
if input != 't':
    print "error 6"
    sys.exit()

while True:
    input = ser.readline()
    print input

