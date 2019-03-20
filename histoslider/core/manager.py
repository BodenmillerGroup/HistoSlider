from PyQt5.QtCore import QModelIndex

from histoslider.core.data import Data
from histoslider.core.decorators import catch_error
from histoslider.core.hub import Hub


class Manager:
    hub: Hub = None
    data: Data = None

    def __init__(self):
        if Manager.hub and Manager.data:
            return
        Manager.hub = Hub()
        Manager.data = Data(Manager.hub)

        # TODO: test code that should be removed later
        Manager.import_slide('/home/anton/Documents/Data/histocat_not_working/20190304_LC_FibroPanelTest_LungAdeno/2019ABTest.mcd')
        Manager.load_slides([Manager.data.workspace_model.index(0, 0)])
        Manager.import_mask('/home/anton/Documents/Data/20190218_Hiertest2/probabilities/BRCA_Trilogy_0_ROI_003_3_a0_ilastik_s2_Probabilities__mask.tiff')

    @staticmethod
    def load_workspace(path: str) -> None:
        Manager.data.load_workspace(path)

    @staticmethod
    def save_workspace(path: str) -> None:
        Manager.data.save_workspace(path)

    @staticmethod
    @catch_error("Could not import slide")
    def import_slide(file_path: str) -> None:
        Manager.data.import_slide(file_path)

    @staticmethod
    # @catch_error("Could not load slide")
    def load_slides(indexes: [QModelIndex]) -> None:
        Manager.data.load_slides(indexes)

    @staticmethod
    @catch_error("Could not close slide")
    def close_slides(indexes: [QModelIndex]) -> None:
        Manager.data.close_slides(indexes)

    @staticmethod
    @catch_error("Could not remove slide")
    def remove_slides(indexes: [QModelIndex]) -> None:
        Manager.data.remove_slides(indexes)

    @staticmethod
    # @catch_error("Could not import slide")
    def import_mask(file_path: str) -> None:
        Manager.data.import_mask(file_path)
