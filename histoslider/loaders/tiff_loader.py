import os

from histoslider.image.slide_type import SlideType
from histoslider.models.slide import Slide


class TiffLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self):
        file_name = os.path.basename(self.file_path)
        slide = Slide(file_name, self.file_path, SlideType.TIFF)
        return slide
