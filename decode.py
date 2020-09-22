#! /bin/python3

import sys
from PIL import Image

STEG_FLAG = [0xB1, 0x0C, 0xFF]
imgName = sys.argv[1]
msg = ''
msgLength = 0
msgLengthHex = ''
x = 0
y = 0

im = Image.open(imgName)
pixelMap = im.load()

def rgb2hex(r, g, b):
    return '0x{:02x}{:02x}{:02x}'.format(b, g, r)

def decodeByte(pixelX,pixelY):
    pixel = pixelMap[pixelX, pixelY]
    pixelHex = rgb2hex(pixel[0], pixel[1], pixel[2])
    decodedByte = int(pixelHex, 16) & 0x0000FF

    global x
    global y
    x += 1
    if x >= im.size[0]:
        x = 0
        y += 1
    if y >= im.size[1]:
        y = 0

    return decodedByte

for byte in STEG_FLAG:
    decodedByte = decodeByte(x,y)
    if byte != decodedByte:
        print("This image does not seem to contain a message.")
        exit(0)

for count in range(24):
    decodedByte = decodeByte(x,y)
    msgLengthHex = '{:06x}'.format(decodedByte) + msgLengthHex

msgLength = int('0x' + msgLengthHex, 16)
for count in range(msgLength):
    msg += chr(decodeByte(x, y))


print(msg)