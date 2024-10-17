import datetime
import time
from typing import Any

import pytz
import requests
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from .text_provider import TextProvider


class MVVProvider(TextProvider):
    """
    :param transport_types List, values UBAHN,REGIONAL_BUS,BUS,TRAM,SBAHN
    :param offset Offset in Minutes
    """

    def __init__(self, matrix, station, title, offset: int = 0, transport_types: list[str] | None = None,
                 fps=30) -> None:
        super().__init__(matrix, fps)
        self.station = station
        self.title = title
        self.transport_types = transport_types
        self.offsetInMinutes = offset
        self.font = ImageFont.truetype("fonts/Berkelium1541.ttf", size=6)
        self.textColor = (150, 150, 20)
        self.titleColor = (100, 200, 200)
        self.tz = pytz.timezone('Europe/Berlin')

    def displayContent(self, t) -> None:
        image = self.createImageFor()
        self.matrix.displayImage(image)
        time.sleep(t)

    def createImageFor(self) -> Image:
        image = Image.new('RGB', self.matrix.getSize(), (0, 0, 0))

        draw = ImageDraw.Draw(image)

        mvgapi = MvvgApi(self.station)
        dep = mvgapi.departures(limit=40, transport_types=self.transport_types)

        dep.sort(key=lambda item: item['realtimeDepartureTime'])
        # print(dep)

        for departure in dep:
            # For some reason, mvg gives you a Unix timestamp, but in milliseconds.
            # Here, we convert it to datetime
            time = datetime.datetime.fromtimestamp(departure['realtimeDepartureTime'] / 1000)
            relative_time = time - datetime.datetime.now()
            if departure['cancelled'] == 'True':
                departure[u'departureTimeMinutes'] = 999999
            else:
                departure[u'departureTimeMinutes'] = relative_time // datetime.timedelta(seconds=60)
                # print(departure)

        title = datetime.datetime.now(self.tz).strftime('%H:%M') + " " + self.title

        ypos = 0
        super().text(draw, (0, ypos), title, self.titleColor)
        ypos = ypos + 7

        for item in filter(lambda x: x["departureTimeMinutes"] >= self.offsetInMinutes, dep):

            # line 
            color_dict = {"U1": (60, 115, 51), "U2": (195, 2, 45), "U3": (237, 103, 32), "U4": (0, 171, 133),
                          "U5": (189, 123, 0), "U6": (0, 101, 176),
                          "S1": (22, 192, 233), "S2": (113, 191, 68), "S3": (123, 16, 125), "S4": (238, 28, 37),
                          "S6": (0, 138, 81), "S7": (150, 56, 51), "S8": (60, 60, 60), "S20": (240, 95, 119),
                          "153": (0, 95, 95), "53": (255, 95, 0), "63": (255, 95, 0), "N43": (0, 60, 60),
                          "N44": (0, 60, 60),
                          "18": (32, 177, 74), "19": (239, 43, 52), "29": (239, 43, 52), "N19": (216, 32, 32)
                          }
            try:
                color = color_dict[item["label"]]
            except KeyError:
                color = (70, 70, 70)

            draw.rectangle([0, ypos, 9, ypos + 4], fill=color)
            super().centeredtext(draw, (5, ypos), item['label'])

            offset = super().text(draw, (11, ypos), item['destination'], self.textColor)

            super().rightaligntext(draw, (image.width + 1, ypos),
                                   "{}min".format(item['departureTimeMinutes']),
                                   self.textColor, bg=(0, 0, 0))

            ypos = ypos + 6
            if ypos + 5 > image.height:
                break
        return image

    def saveTestImage(self) -> None:
        image = self.createImageFor()
        image.save("mvv1.png", "PNG")


class MvvgApi:
    station: str

    def __init__(self, station: str):
        self.station = station.strip()

    def departures(self, limit: int = 40, transport_types: list[str] | None = None) -> list[
        dict[str, Any]]:
        if transport_types is None:
            transport_types = ["UBAHN", "REGIONAL_BUS", "BUS", "TRAM", "SBAHN"]

        params = {
            "globalId": self.station,
            "limit": limit,
            "transportTypes": str.join(',', transport_types),
        }
        result = requests.get("https://mvg.de/api/bgw-pt/v3/departures", params=params)

        json = result.json()
        return json
