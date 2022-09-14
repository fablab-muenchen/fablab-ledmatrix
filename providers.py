from email.mime import image
from mimetypes import init
import time
import numpy as np
import utils
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from matrix import Matrix

from mss import mss

class Provider:
    def __init__(self, matrix, fps=10) -> None:
        self.matrix = matrix
        self.fps = fps

    def displayContent(self, t) -> None:
        array = utils.get_gradient_3d(self.matrix.getWidth(),
                                      self.matrix.getHight(),
                                      (0, 0, 192),
                                      (255, 255, 64),
                                      (True, False, False))
        self.matrix.displayImage(Image.fromarray(np.uint8(array)))
        time.sleep(t)


class ScreenProvider(Provider):
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

class TextProvider(Provider):
    def __init__(self, matrix, text, fps=30, background=(0, 0, 0)) -> None:
        super().__init__(matrix, fps)
        self.text = text
        self.background = background

    def displayContent(self, t) -> None:
        image = Image.new('RGB', self.matrix.getSize(), self.background)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((0, 0),self.text,(255,255,255),font=font)
        self.matrix.displayImage(image)
        time.sleep(t)
