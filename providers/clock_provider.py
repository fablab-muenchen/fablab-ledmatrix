import time
from datetime import datetime

import pytz
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from .text_provider import TextProvider


class ClockProvider(TextProvider):
    def __init__(self, matrix, fps=5) -> None:
        super().__init__(matrix, fps)
        self.font = ImageFont.truetype("fonts/FiraCode-Regular.otf", size=20)
        self.textColor = (150, 150, 20)
        self.titleColor = (100, 200, 200)
        self.tz = pytz.timezone('Europe/Berlin')

    def displayContent(self, t) -> None:
        starttime = time.time()
        while time.time() < (starttime + float(t)):
            image = self.createImageFor()
            self.matrix.displayImage(image)
            time.sleep(1 / self.fps)

    def createImageFor(self) -> Image:
        image = Image.new('RGB', self.matrix.getSize(), (0, 0, 0))
        draw = ImageDraw.Draw(image)
        (x, y) = self.matrix.getCenter()
        y = y - round(self.font.size / 2) - 4

        super().centeredtext(draw, (x, y), datetime.now(self.tz).strftime("%H:%M:%S"))
        return image
