from typing import List

import cv2
import numpy as np
from PyQt5.QtWidgets import QWidget
from pyqtgraph import ImageView, ScaleBar

from histoslider.core.manager import Manager
from histoslider.core.view_mode import ViewMode
from histoslider.image.channel_image_item import ChannelImageItem
from histoslider.image.utils import scale_image, apply_mask


class BlendView(ImageView):
    def __init__(self, parent: QWidget):
        ImageView.__init__(self, parent, "BlendView")
        self.getHistogramWidget().hide()
        self.ui.roiBtn.hide()
        self.ui.menuBtn.hide()

        self.scale = ScaleBar(size=10, suffix='μm')
        self.scale.setParentItem(self.getView())
        self.scale.anchor((1, 1), (1, 1), offset=(-20, -20))
        self.scale.hide()

        self._show_mask = False
        self.items: List[ChannelImageItem] = None

    def clear(self):
        super().clear()
        self.items = None

    def set_images(self, items: List[ChannelImageItem]):
        self.items = items
        if items is None or len(items) == 0:
            return
        blend_image = 0
        levels = []
        if len(items) == 1:
            blend_image = items[0].image
            levels.append(items[0].channel.settings.levels)
        else:
            for item in items:
                image = scale_image(item.image, item.channel.settings.max, item.channel.settings.levels)
                blend_image = cv2.addWeighted(blend_image, 0.5, image, 0.5, 0.0) if Manager.data.blend_mode == 'Weighted' else cv2.add(blend_image, image)
                levels.append(item.channel.settings.levels)
        if self._show_mask and Manager.data.selected_mask is not None:
            mask_image = Manager.data.selected_mask.image
            # if Manager.data.view_mode is ViewMode.RGB:
            #     mask_image = cv2.cvtColor(mask_image, cv2.COLOR_GRAY2RGB)
            # if mask_image.shape == blend_image.shape:
                # blend_image = cv2.addWeighted(blend_image, 0.8, mask_image, 0.2, 0.0) if Manager.data.blend_mode == 'Weighted' else cv2.add(blend_image, mask_image)
            blend_image = apply_mask(blend_image, mask_image)
        self.setImage(blend_image, autoHistogramRange=False, autoRange=False)
        self.setLevels(*max(levels))

    def refresh_images(self):
        self.set_images(self.items)

    def show_scale_bar(self, state: bool):
        if state:
            self.scale.show()
        else:
            self.scale.hide()

    def set_show_mask(self, state: bool):
        self._show_mask = state
        self.refresh_images()
