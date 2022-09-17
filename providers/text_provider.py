import time
import numpy as np
#import providers.utils as utils
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from .default_provider import DefaultProvider

class TextProvider(DefaultProvider):
    def __init__(self, matrix, text, fps=30, background=(0, 0, 0)) -> None:
        super().__init__(matrix, fps)
        self.text = text
        self.font = ImageFont.truetype("fonts/Berkelium1541.ttf", size=6)
        self.background = background

    def displayContent(self, t) -> None:
        image = Image.new('RGB', self.matrix.getSize(), self.background)
        draw = ImageDraw.Draw(image)
        font = ImageFont.load_default()
        # draw.text((x, y),"Sample Text",(r,g,b))
        draw.text((0, 0),self.text,(255,255,255),font=font)
        self.matrix.displayImage(image)
        time.sleep(t)

    def text(self, draw, pos, text, color=(255,255,255)) -> int:
        pixels = draw.textlength(text, font=self.font)
        draw.text(pos, text, color, font=self.font)
        return int(round(pixels))

    def centeredtext(self, draw, pos, text, color=(255,255,255)) -> None:
        pixels = draw.textlength(text, font=self.font)
        (x,y) = pos
        pos = (round(x-pixels/2+0.5), y)
        draw.text(pos, text, color, font=self.font)

    def rightaligntext(self, draw, pos, text, color=(255,255,255), bg=None) -> None:
        pixels = draw.textlength(text, font=self.font)
        (x,y) = pos
        pos = (round(x-pixels), y)
        if bg:
            draw.rectangle([(x-pixels-1,y), (x,y+6)], fill=bg)
        draw.text(pos, text, color, font=self.font)