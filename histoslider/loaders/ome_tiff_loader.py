import os

from imctools.io.ometiffparser import OmetiffParser

from histoslider.image.slide_type import SlideType
from histoslider.models.acquisition import Acquisition
from histoslider.models.acquisition_channel import AcquisitionChannel
from histoslider.models.slide import Slide


class OmeTiffLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self):
        file_name = os.path.basename(self.file_path)
        ome = OmetiffParser(self.file_path)
        slide = Slide(file_name, self.file_path, SlideType.OMETIFF)
        imc_ac = ome.get_imc_acquisition()
        acquisition = Acquisition(imc_ac.image_ID, imc_ac.image_description)
        slide.add_acquisition(acquisition)
        for i in range(imc_ac.n_channels):
            img = imc_ac.get_img_by_label(imc_ac.channel_labels[i])
            channel = AcquisitionChannel(imc_ac.channel_labels[i], imc_ac.channel_metals[i], imc_ac.channel_mass[i], img)
            acquisition.add_channel(channel)

        return slide
