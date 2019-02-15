import os

from imctools.io.ometiffparser import OmetiffParser

from histoslider.image.slide_type import SlideType
from histoslider.models.acquisition_data import AcquisitionData
from histoslider.models.channel_data import ChannelData
from histoslider.models.slide_data import SlideData


class OmeTiffLoader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load(self):
        file_name = os.path.basename(self.file_path)
        ome = OmetiffParser(self.file_path)
        slide_data = SlideData(file_name, self.file_path, SlideType.OMETIFF)
        imc_ac = ome.get_imc_acquisition()
        acquisition_data = AcquisitionData(imc_ac.image_ID, imc_ac.image_description)
        slide_data.add_acquisition(acquisition_data)
        for i in range(imc_ac.n_channels):
            img = imc_ac.get_img_by_label(imc_ac.channel_labels[i])
            channel_data = ChannelData(imc_ac.channel_labels[i], imc_ac.channel_metals[i], imc_ac.channel_mass[i], img)
            acquisition_data.add_channel(channel_data)

        return slide_data
