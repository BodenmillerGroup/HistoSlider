import os

import imctools.io.mcdparser as mcdparser

from histoslider.image.slide_type import SlideType
from histoslider.models.acquisition import Acquisition
from histoslider.models.channel import Channel
from histoslider.models.slide import Slide


class McdLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self):
        with mcdparser.McdParser(self.file_path) as mcd:
            file_name = os.path.basename(self.file_path)
            slide = Slide(file_name, self.file_path, SlideType.MCD)
            for id in mcd.acquisition_ids:
                description = mcd.get_acquisition_description(id)
                imc_ac = mcd.get_imc_acquisition(id, description)
                acquisition = Acquisition(imc_ac.image_description, imc_ac.image_description)
                slide.add_acquisition(acquisition)
                for i in range(imc_ac.n_channels):
                    img = imc_ac.get_img_by_label(imc_ac.channel_labels[i])
                    channel = Channel(imc_ac.channel_labels[i], imc_ac.channel_metals[i], imc_ac.channel_mass[i], img)
                    acquisition.add_channel(channel)
            return slide
