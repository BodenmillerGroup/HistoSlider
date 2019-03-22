from typing import List

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QImage
from PyQt5.QtWidgets import QWidget
from pyqtgraph import ViewBox, GraphicsView, GraphicsLayout, ImageItem, ScaleBar
from qimage2ndarray import array2qimage, rgb_view

from histoslider.core.manager import Manager
from histoslider.core.view_mode import ViewMode
from histoslider.core.workers.worker import Worker
from histoslider.image.channel_image_item import ChannelImageItem
from histoslider.image.utils import scale_image, apply_mask


class BlendView(GraphicsView):
    def __init__(self, parent: QWidget):
        GraphicsView.__init__(self, parent)
        layout = GraphicsLayout()
        self.setCentralItem(layout)

        self._image_item = ImageItem()
        self.viewbox = ViewBox(layout, lockAspect=True, invertY=True)
        self.viewbox.addItem(self._image_item)
        layout.addItem(self.viewbox)

        self.scale = ScaleBar(size=10, suffix='μm')
        self.scale.setParentItem(self.viewbox)
        self.scale.anchor((1, 1), (1, 1), offset=(-20, -20))
        self.scale.hide()

        self._show_mask = False
        self.blend_mode = QPainter.CompositionMode_Screen
        self.items: List[ChannelImageItem] = None

    def clear(self):
        self.viewbox.clear()
        self.items = None

    def set_images(self, items: List[ChannelImageItem]):
        self.items = items
        if items is None or len(items) == 0:
            return
        images = []
        for item in items:
            image = scale_image(item.image, item.channel.settings.max, item.channel.settings.levels)
            images.append(array2qimage(image, normalize=False))

        self._draw_images(images)

    def _draw_images(self, images: List[QImage]):
        result = QImage(images[0].size(), QImage.Format_ARGB32_Premultiplied)
        painter = QPainter(result)
        painter.setCompositionMode(QPainter.CompositionMode_Source)
        painter.fillRect(images[0].rect(), Qt.transparent)
        painter.setCompositionMode(self.blend_mode)
        for i in images:
            painter.drawImage(0, 0, i)
        painter.end()

        self._image_item.setImage(rgb_view(result))

    def refresh_images(self):
        self.set_images(self.items)

    def set_blend_mode(self, modename: str):
        self.blend_mode = getattr(QPainter, 'CompositionMode_' + modename)
        self.set_images(self.items)

    def show_scale_bar(self, state: bool):
        if state:
            self.scale.show()
        else:
            self.scale.hide()

    def progress_fn(self, n):
        print("%d%% done" % n)

    def process_result(self, result):
        print("PROCESS RESULTS!")
        if self._show_mask:
            self._image_item.setImage(result)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def show_mask(self, state: bool):
        self._show_mask = state
        if not state:
            self.refresh_images()
            return

        if Manager.data.selected_mask is None or Manager.data.view_mode is ViewMode.GREYSCALE:
            return

        mask = Manager.data.selected_mask.image
        blend_image = self._image_item.image

        # Pass the function to execute
        worker = Worker(apply_mask, image=blend_image, mask=mask)  # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.process_result)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        Manager.threadpool.start(worker)
