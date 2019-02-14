from histoslider.core.hub import Hub
from histoslider.core.message import ShowItemChangedMessage
from histoslider.models.workspace_model import WorkspaceModel


class DataManager:
    workspace_model: WorkspaceModel = None
    hub: Hub = None

    def __init__(self):
        if DataManager.workspace_model and DataManager.hub:
            return
        DataManager.workspace_model = WorkspaceModel()
        DataManager.hub = Hub()
        DataManager.workspace_model.show_item_changed.connect(DataManager._on_show_item_changed)

    @staticmethod
    def load_workspace(path: str):
        DataManager.workspace_model.beginResetModel()
        DataManager.workspace_model.load_workspace(path)
        DataManager.workspace_model.endResetModel()

    @staticmethod
    def save_workspace(path: str):
        DataManager.workspace_model.save_workspace(path)

    @staticmethod
    def _on_show_item_changed(item):
        DataManager.hub.broadcast(ShowItemChangedMessage(DataManager, item))
