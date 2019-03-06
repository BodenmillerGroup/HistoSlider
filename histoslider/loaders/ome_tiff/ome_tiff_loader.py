from __future__ import annotations

import os

from imctools.io.ometiffparser import OmetiffParser

from histoslider.loaders.loader import Loader
from histoslider.models.acquisition import Acquisition
from histoslider.models.channel import Channel
from histoslider.models.slide import Slide


class OmeTiffLoader(Loader):

    @classmethod
    def load(cls, slide: Slide) -> Slide:
        slide_path = slide.slide_path
        ome = OmetiffParser(slide_path)
        file_name = os.path.basename(slide_path)
        slide.meta = ome.meta_dict
        imc_acquisition = ome.get_imc_acquisition()
        meta = dict()
        meta["Origin"] = imc_acquisition.origin
        meta["ImageDescription"] = imc_acquisition.image_description
        acquisition = Acquisition("Acquisition", meta)
        slide.addChild(acquisition)
        for i in range(imc_acquisition.n_channels):
            img = imc_acquisition.get_img_by_label(imc_acquisition.channel_labels[i])
            meta = dict()
            meta['Label'] = imc_acquisition.channel_labels[i]
            meta['Metal'] = imc_acquisition.channel_metals[i]
            meta['Mass'] = imc_acquisition.channel_mass[i]
            channel = Channel(imc_acquisition.channel_labels[i], meta, img)
            acquisition.add_channel(channel)
        return slide

    @classmethod
    def close(cls, slide: Slide):
        raise NotImplementedError
