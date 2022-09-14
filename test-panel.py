#!/usr/bin/env python3

import sys
import subprocess
import select
import requests
import time
from PIL import Image
from matrix import Matrix

#import cv2
#from cv2 import VideoCapture
import numpy as np

from mss import mss

import matplotlib.pyplot as plt

SIZE = (96,64)

m = Matrix()

red = Image.new('RGB', SIZE, (255, 0, 0))
green = Image.new('RGB', SIZE, (0, 255, 0))
blue = Image.new('RGB', SIZE, (0, 0, 255))
white = Image.new('RGB', SIZE, (255, 255, 255))
# m.displayImage(white)
m.displayImage(red)
m.start()

# sys.exit()

# SCREEN CAP
sct = mss()
monitor = sct.monitors[1]
left = monitor["left"]
right = monitor["width"]
top = monitor["top"]
bottom = monitor["height"]
bbox = (left, top, right, bottom)

while True:
    sct_img = sct.grab(bbox)
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
    m.displayImage(image)
    time.sleep(0.03)



# WEBCAM
#cam = VideoCapture(0)
#while not cam.isOpened():
#    time.sleep(0.1)
#
#while True:
#    retval, image = cam.read()
#    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#    image = Image.fromarray(image)
#    m.displayImage(image)
#    time.sleep(0.03)
#

# PARTY MODE
while True:
    time.sleep(1)
    m.displayImage(red)
    time.sleep(1)
    m.displayImage(green)
    time.sleep(1)
    m.displayImage(blue)