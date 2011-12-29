#!/usr/bin/env python

#    LPC3250loader.py, a simple image/program loader for LPC3250
#
#    Copyright (C) 2011 Alexandre Belloni
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import sys, os, serial, getopt

loadaddr = 0x00000000
imgaddr = 0x80000004

serialport = "/dev/ttyUSB0"
burnerfile = None
imagefile = None


def usage():
    print "%s programfile" % (sys.argv[0])

try:
    opts, args = getopt.getopt(sys.argv[1:], "a:i:l:p:hv", ["help", "imgaddress=", "image=", "loadaddress=", "port="])
except getopt.GetoptError, err:
    print str(err)
    usage()
    sys.exit(2)
verbose = False

if len(args) != 1:
    usage()
    sys.exit()

burnerfile = args[0]

for o, a in opts:
    if o == "-v":
        verbose = True
    elif o in ("-h", "--help"):
        usage()
        sys.exit()
    elif o in ("-i", "--image"):
        imagefile = a
    elif o in ("-p", "--port"):
        serialport = a
    #TODO addresses
    else:
        usage()
        sys.exit()

print "%s, %s, %s" % (burnerfile, imagefile, serialport)

if not os.path.exists(burnerfile):
    sys.stderr.write("Couldn't find " + burnerfile + "\n")
    sys.exit(1)

if imagefile and not os.path.exists(imagefile):
    sys.stderr.write("Couldn't find " + imagefile + "\n")
    sys.exit(1)

ser = serial.Serial(serialport, 115200, timeout=300)

print "Waiting for BOOTID..."

while True:
    input = ser.read()
    print "Got %c(%d)" % (input, ord(input))
    if input == '5':
        break

ser.write('A')
print "Found! Sent char A"


print "Waiting for 2nd BOOTID..."

input = 0
input = ser.read()
print "Got %c(%d)" % (input, ord(input))
if input != '5':
    print "error 2"
    sys.exit()

ser.write('U3')
print "Found! Sent chars U3"

print "Waiting for confirmation..."

input = 0
input = ser.read()
print "Got %c(%d)" % (input, ord(input))
if input != 'R':
    print "error 3"
    sys.exit()

print "Found! Sent chars U3"

print "Sending load address: %d" % (loadaddr)
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

# Burner is getting executed
print "Waiting for burner..."
input = ser.read()
print "Got %c(%d)" % (input, ord(input))
if input != 'X':
    print "error 4"
    sys.exit()

ser.write('p')
print "OK. Sent char p"

print "Sending Image address: %d" % (imgaddr)
val = imgaddr
for i in range(4):
    ser.write(chr(val&0xFF))
    val = val >> 8

size = os.path.getsize(imagefile)
print "Sending Filesize: %d" % (size)
val = size
for i in range(4):
    ser.write(chr(val&0xFF))
    val = val >> 8

input = ser.read()
print "Got %c(%d)" % (input, ord(input))
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
print "Got %c(%d)" % (input, ord(input))
if input != 't':
    print "error 6"
    sys.exit()

print "Everything OK, flashing... press (Ctrl+C) to quit"
while True:
    input = ser.readline()
    print input

