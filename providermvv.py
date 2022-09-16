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
from  utils import color_hex2triplet, color_mult



class ProviderMVV(Provider):
    def __init__(self, matrix, fps=30) -> None:
        super().__init__(matrix, fps)
        self.font = ImageFont.truetype("fonts/Berkelium1541.ttf", size=6)
        self.textColor = (150,150,20)
        self.titleColor = (100,200,200)

    def displayContent(self, t) -> None:
        image = self.createImage1()
        self.matrix.displayImage(image)
        time.sleep(t)
        image = self.createImage2()
        self.matrix.displayImage(image)
        time.sleep(t)
        
    def createImage1(self) -> Image:
        image = self.createImageFor('de:09162:1150', "ABFAHRTEN Heimeranplatz", 
          lambda x: x['departureTimeMinutes'] >= 5 and
                    ( x['label'].startswith("U") or x['label'].startswith("S")))
        return image
        
    def createImage2(self) -> Image:
        image = self.createImageFor('de:09162:8', "ABFAHRTEN Donnersb.Brücke",
          lambda x: x['departureTimeMinutes'] >= 5 and x['label'].startswith("S"))
        return image

    def createImageFor(self, station, title, labelFilter) -> Image:
        image = Image.new('RGB', self.matrix.getSize(), (0,0,0))
        draw = ImageDraw.Draw(image)

        dep = mvg_api.get_departures(station)
        dep.sort(key=lambda item: item['departureTimeMinutes'])
        #print(dep)
        
        ypos = 0;
        self.text(draw, (0, ypos), title, self.titleColor)
        ypos = ypos+7
        
        for item in filter(lambda x: labelFilter(x), dep): 
            #print(item)         
            
            # line
            color = color_hex2triplet(item['lineBackgroundColor'])
            color = color_mult(color, 0.75)
            draw.rectangle([0,ypos, 9,ypos+4], fill=color)
            self.centeredtext(draw, (5, ypos), item['label'])
            
            offset = self.text(draw, (11, ypos), item['destination'], self.textColor)
              
            self.rightaligntext(draw, (image.width+1, ypos), 
              "{}min".format(item['departureTimeMinutes']), 
              self.textColor, bg=(0,0,0))
            
            # lass ich weg, ist in departureTimeMinutes schon einberechnet
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
          
        
    def saveTestImage(self) -> None:
        image = self.createImage1()
        image.save("mvv1.png", "PNG")
        image = self.createImage2()
        image.save("mvv2.png", "PNG")
