import socket 


class SubnetBroadcaster(object):
    """This class is used to broadcast messages out to the network. So far this is the only way of communication.
    Note: This class can (and should) be used with a context manager (aka a with statement).
    This takes care of socket creation and destruction.

    Args:
        listener_port (int): Port the app uses to communicate with peers
        GOODBYE_MSG (str): msg send to signal that this app is leaving the network (in a regular way)
    """
    def __init__(self, listener_port, goodbye_msg):
        self.listener_port = listener_port
        self.GOODBYE_MSG = goodbye_msg

        if not getattr(self, 'broadcast_socket', None):
            self.__enter__()

    def __enter__(self):
        """ Used by context manager ONLY! """
        self._make_broadcast_socket()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """ Used by context manager ONLY! """
        self.terminate()

    def _make_broadcast_socket(self):
        """ Creates a broadcast socket. """
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)

    def _destroy_broadcast_socket(self):
        """ Destroys the broadcast socket. """
        self.broadcast_socket.close()

    def send(self, msg):
        """ Send a message over the broadcast.

        Args:
            msg (str): message to send
        """
        target = ('<broadcast>', self.listener_port)
        self.broadcast_socket.sendto(msg.encode(), target)

    def terminate(self):
        """ Use this func to properly destroy this class if you don't use a context manager. """
        self.send_goodbye_msg()
        self._destroy_broadcast_socket()

    def send_goodbye_msg(self):
        """ Send goodbye message. This is the proper way to close app and inform peers. """
        self.send(self.GOODBYE_MSG)

