import time
import numpy as np
import providers.utils as utils
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from .default_provider import DefaultProvider

class ScreenProvider(DefaultProvider):
    def __init__(self, matrix, fps=30) -> None:
        super().__init__(matrix, fps)

    def displayContent(self, t) -> None:
        starttime = time.time()
        sct = mss()
        monitor = sct.monitors[1]
        left = monitor["left"]
        right = monitor["width"]
        top = monitor["top"]
        bottom = monitor["height"]
        bbox = (left, top, right, bottom)

        while time.time() < (starttime + float(t)):
            sct_img = sct.grab(bbox)
            # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            self.matrix.displayImage(image)
            time.sleep(1/self.fps)