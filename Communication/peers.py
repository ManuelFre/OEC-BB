from datetime import datetime as dt


class NetworkNode(object):
    """ Introduced NetworkNode objects for a variety of reasons. E.g.
    * The are easy to check for their last_seen prop.
    * Future proofing

    Args:
        ip (str): The nodes ip
        port (int): The nodes port
        banner (str): Optional. Can be used to display additional information. * is used to mark self.
    """
    def __init__(self, ip, port, banner=None):
        self.ip = ip
        self.port = port
        self.banner = banner or ''
        self._messages = []
        self.last_seen = dt.utcnow()

    def get_messages(self):
        return self._messages

    def add_message(self, message):
        self._messages.append(Message(message))
        self.last_seen = dt.utcnow()


class Message(object):
    """ This is how messages are represented. Currently serves no purpose. Just here for future proofing.

    Args:
        msg (str): message text
        timestamp (Datetime obj): Default: Datetime.utcnow()
    """
    def __init__(self, msg, timestamp=None):
        self.msg = msg
        self.timestamp = timestamp or dt.utcnow()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.msg
