import threading
import socket
from Misc.helpers import debug_print


class MessageRCV(object):
    """ This class is used to receive messages send by the broadcaster.

    Args:
        message_callback_func (func pointer): func to call when a msg was received
        port (int): Port the app uses to communicate with peers
    """
    def __init__(self, message_callback_func, port):
        self.port = port

        self._server_thread = None
        self._server_socket = None

        self.message_callback_func = message_callback_func

        self.is_listening = False

    def start_listening(self):
        """ Starts a (threaded) listener function. """
        if not self.is_listening:
            debug_print('Listener: Starting service ...')
            self._stop = threading.Event()

            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self._server_socket.bind(('', self.port))

            self.is_listening = True
            self._server_thread = threading.Thread(target=self._listen_for_broadcasts)
            self._server_thread.setDaemon(True)
            self._server_thread.start()
            debug_print('Listener: Started ...')

        else:
            debug_print('Listener: Service already running. Nothing was started.')

    def stop_listening(self):
        """ Stoppes the threaded listener function. """
        if self.is_listening:
            debug_print("Listener: Stopping service ...")
            self._stop.set()
            self._server_thread.join(timeout=0)
            self.is_listening = False
            self._server_socket.close()
            debug_print("Listener: Stopped")

        else:
            debug_print("Listener: Service wasn't running. Nothing to stop.")

    def _listen_for_broadcasts(self):
        """ Listenes for broadcasts and sends them to the msg received callback func. """
        while not self._stop.is_set():
            message, address = self._server_socket.recvfrom(512)
            self.message_callback_func(message.decode(), address)
