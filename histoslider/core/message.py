from typing import Dict

from histoslider.models.base_data import BaseData
from histoslider.models.channel import Channel


class Message:

    """
    Base class for messages that the hub handles.

    Each message represents a specific kind of event. After clients
    register to a hub, the subscribe to specific message classes, and
    will only receive those kinds of messages.

    The message class family is hierarchical, and a client subscribing
    to a message class implicitly subscribes to all of its subclasses.

    :attr sender: The object which sent the message
    :attr tag: An optional string describing the message
    """

    def __init__(self, sender, tag=None):
        """Create a new message

        :param sender: The object sending the message
        :param tag: An optional string describing the message
        """
        self.sender = sender
        self.tag = tag

    def __str__(self):
        return '%s: %s\n\t Sent from: %s' % (type(self).__name__,
                                             self.tag or '',
                                             self.sender)


class ErrorMessage(Message):

    """ Used to send general purpose error messages """
    pass


class SelectedTreeNodeChangedMessage(Message):

    """ Indicates that the selected TreeView node has changed """

    def __init__(self, sender, node: BaseData, tag=None):
        Message.__init__(self, sender, tag=tag)
        self.node = node


class CheckedChannelChangedMessage(Message):

    """ Indicates that the selected channel has changed """

    def __init__(self, sender, channel: Channel, tag=None):
        Message.__init__(self, sender, tag=tag)
        self.channel = channel


class CheckedChannelsChangedMessage(Message):

    """ Indicates that checked channels are changed """

    def __init__(self, sender, channels: Dict[str, Channel], tag=None):
        Message.__init__(self, sender, tag=tag)
        self.channels = channels


class SlideImportedMessage(Message):

    """ Indicates that the slide has been imported """
    pass


class SlideRemovedMessage(Message):

    """ Indicates that the slide has been removed """
    pass


class SlideLoadedMessage(Message):

    """ Indicates that the slide has been loaded """
    pass


class SlideUnloadedMessage(Message):

    """ Indicates that the slide has been unloaded """
    pass
