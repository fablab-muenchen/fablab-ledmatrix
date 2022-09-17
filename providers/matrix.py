#!/usr/bin/env python3

import socket
import time
from PIL import Image

UDP_IP = "10.100.198.159" #"rgbmatrix.local"
UDP_PORT = 9998
SIZE = (96,64)

# on macOS: sudo sysctl -w net.inet.udp.maxdgram=65535
# net.inet.udp.maxdgram: 9216 -> 65535

class Matrix:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.t = None
    
    def displayImage(self, im):
        # im = Image.open("./album.jpg")
        im = im.transpose(Image.FLIP_LEFT_RIGHT)
        #im = im.transpose(Image.FLIP_TOP_BOTTOM)
        im.thumbnail(SIZE, Image.ANTIALIAS)

        background = Image.new('RGB', SIZE, (0, 0, 0))
        background.paste(im, (int((SIZE[0] - im.size[0]) / 2), int((SIZE[1] - im.size[1]) / 2)))

        self.imgBytes = background.tobytes()
        self.sock.sendto(self.imgBytes, (UDP_IP, UDP_PORT))       

    def getWidth(self):
        return SIZE[0]

    def getHight(self):
        return SIZE[1]
    
    def getSize(self):
        return SIZE

    def getCenter(self):
        return (round(SIZE[0]/2),round(SIZE[1]/2))