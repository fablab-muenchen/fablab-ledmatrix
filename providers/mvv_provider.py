import time
import datetime
import pytz
import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 
from .text_provider import TextProvider

from mvg import MvgApi
from  providers.utils import color_hex2triplet, color_mult



class MVVProvider(TextProvider):
    def __init__(self, matrix, station, title, station_filter,fps=30) -> None:
        super().__init__(matrix, fps)
        self.station = station
        self.title = title
        self.station_filter = station_filter
        self.font = ImageFont.truetype("fonts/Berkelium1541.ttf", size=6)
        self.textColor = (150,150,20)
        self.titleColor = (100,200,200)
        self.tz = pytz.timezone('Europe/Berlin')

    def displayContent(self, t) -> None:
        image = self.createImageFor(self.station, self.title, self.station_filter)
        self.matrix.displayImage(image)
        time.sleep(t)

        
    def createImageFor(self, station, title, labelFilter) -> Image:
        image = Image.new('RGB', self.matrix.getSize(), (0,0,0))
        draw = ImageDraw.Draw(image)

        station = MvgApi.station(station)
        if not station:
            return
            
        mvgapi = MvgApi(station['id'])
        dep = mvgapi.departures(limit=40)
        
        dep.sort(key=lambda item: item['time'])
        #print(dep)
        
        for departure in dep:
            # For some reason, mvg gives you a Unix timestamp, but in milliseconds.
            # Here, we convert it to datetime
            time = datetime.datetime.fromtimestamp(departure['time'])
            relative_time = time - datetime.datetime.now()
            if departure['cancelled']=='True':
                departure[u'departureTimeMinutes'] = 999999        
            else:
                departure[u'departureTimeMinutes'] = relative_time // datetime.timedelta(seconds=60)   
            #print(departure)     

        title = datetime.datetime.now(self.tz).strftime('%H:%M') + " " + title
        
        ypos = 0;
        super().text(draw, (0, ypos), title, self.titleColor)
        ypos = ypos+7
        

        for item in filter(lambda x: labelFilter(x), dep): 
            #print(item)         
            
            # line
            #color = color_hex2triplet(item['lineBackgroundColor'])
            #color = color_mult(color, 0.75)
            color = (70,70,70)
            draw.rectangle([0,ypos, 9,ypos+4], fill=color)
            super().centeredtext(draw, (5, ypos), item['line'])
            
            offset = super().text(draw, (11, ypos), item['destination'], self.textColor)
              
            super().rightaligntext(draw, (image.width+1, ypos), 
              "{}min".format(item['departureTimeMinutes']), 
              self.textColor, bg=(0,0,0))
                        
            ypos = ypos+6
            if ypos+5>image.height:
                break;
        return image
          
        
    def saveTestImage(self) -> None:
        image = self.createImageFor(self.station, self.title, self.station_filter)
        image.save("mvv1.png", "PNG")
