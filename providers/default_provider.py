from email.mime import image
from mimetypes import init
import time
import numpy as np
import providers.utils as utils
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

from mss import mss
class DefaultProvider:
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