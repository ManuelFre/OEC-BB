import socket 


# this class can and should be used with a context manager (aka a with statement)
class SubnetBroadcaster(object):
    def __init__(self, listener_port, goodbye_msg):
        self.listener_port = listener_port
        self.GOODBYE_MSG = goodbye_msg

    def __enter__(self):
        self._make_broadcast_socket()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self._destroy_broadcast_socket()

    def _make_broadcast_socket(self):
        self.broadcast_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.broadcast_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)

    def _destroy_broadcast_socket(self):
        self.broadcast_socket.close()

    def sent(self, msg):
        target = ('<broadcast>', self.listener_port)
        self.broadcast_socket.sendto(msg.encode(), target)

    def sent_goodbye_msg(self):
        self.sent(self.GOODBYE_MSG)


# with SubnetBroadcaster(48881, ) as c:
#     c.sent("TEST")
