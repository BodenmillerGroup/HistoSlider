from __future__ import annotations

from skimage.io import imread

from histoslider.loaders.loader import Loader
from histoslider.models.mask import Mask


class MaskLoader(Loader):

    @classmethod
    def load(cls, mask: Mask) -> Mask:
        path = mask.path
        image = imread(path, plugin='pil')
        mask._image = image
        meta = dict()
        meta['MaxX'] = image.shape[1]
        meta['MaxY'] = image.shape[0]
        mask.meta = meta
        return mask

    @classmethod
    def close(cls, mask: Mask):
        raise NotImplementedError
