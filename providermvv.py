import time
import numpy as np
import utils
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from matrix import Matrix
from mss import mss
from providers import Provider

import mvg_api
from  utils import color_hex2triplet

class ProviderMVV(Provider):
    def __init__(self, matrix, fps=30) -> None:
        super().__init__(matrix, fps)
        self.font = ImageFont.truetype("fonts/Berkelium1541.ttf", size=6)

    def displayContent(self, t) -> None:
        image = self.createImage()
        self.matrix.displayImage(image)
        time.sleep(t)
        
    def createImage(self) -> Image:
        image = Image.new('RGB', self.matrix.getSize(), (0,0,0))
        draw = ImageDraw.Draw(image)
        
        dep = mvg_api.get_departures('de:09162:1150', timeoffset=5)
        ypos = 0;
        self.text(draw, (0, ypos), "ABFAHRTEN Heimeranplatz",(127,255,255))
        ypos = ypos+7
        
        for item in filter(lambda x: x['label']=="U5" or x['label']=="U4", dep): 
            #print(item)         
            color = color_hex2triplet(item['lineBackgroundColor'])
            self.text(draw, (0, ypos), item['label'], color)
            txt = "{} {}min".format(
              item['destination'], 
              item['departureTimeMinutes']
              )
            offset = self.text(draw, (10, ypos), txt)
            #if item['delay']>-1:
            #    self.text(draw, (10+offset, ypos), "+{}".format(item['delay']), (255,0,0))
            ypos = ypos+6
            if ypos+5>image.height:
                break;
        return image
        
    def text(self, draw, pos, text, color=(255,255,255)) -> int:
        pixels = draw.textlength(text, font=self.font)
        draw.text(pos, text, color, font=self.font)
        return int(round(pixels))
        
    def saveTestImage(self) -> None:
        image = self.createImage()
        image.save("mvv.png", "PNG")
