#! /bin/python3

import sys
from PIL import Image

STEG_FLAG = [0xB1, 0x0C, 0xFF]
msg = sys.argv[1]
imgName = sys.argv[2]
msgLength = len(msg)

im = Image.open(imgName)
pixelMap = im.load()
x = 0
y = 0


def rgb2hex(r, g, b):
    return '0x{:02x}{:02x}{:02x}'.format(r, g, b)

def encodeByte(pixelX, pixelY, byte):
    pixel = pixelMap[pixelX, pixelY]
    pixelHex = rgb2hex(pixel[0],pixel[1],pixel[2])
    encodedByte = (int(pixelHex, 16) & 0xFFFF00) | byte
    encodedByteHex = '0x{:06x}'.format(encodedByte)
    pixelMap[pixelX, pixelY] = int(encodedByteHex, 16)
    print(pixelHex, hex(byte), encodedByteHex)

    global x
    global y
    x += 1
    if x >= im.size[0]:
        x = 0
        y += 1
    if y >= im.size[1]:
        y = 0

for byte in STEG_FLAG:
    encodeByte(x,y,byte)

for count in range(24):
    byte = msgLength >> count * 8
    encodeByte(x,y,byte)

for byte in list(msg):
    encodeByte(x,y,ord(byte))

imgParts = imgName.rsplit('.', 1)
im.save(imgParts[0] + '-steg.' + imgParts[1])