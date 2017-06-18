import threading
import socket


class MessageRCV(object):
    def __init__(self, message_callback_func, port):
        self.port = port

        self._stop = threading.Event()
        self._server_thread = None
        self._server_socket = None

        self.message_callback_func = message_callback_func

        self.do_listen = False

    def start_listening(self):
        if not self.do_listen:
            print('Listener: Starting service ...')
            self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self._server_socket.bind(('', self.port))

            self.do_listen = True
            self._server_thread = threading.Thread(target=self._listen_for_broadcasts)
            self._server_thread.setDaemon(True)
            self._server_thread.start()
            print('Listener: Started ...')

        else:
            print('Listener: Service already running. Nothing was started.')

    def stop_listening(self):
        if self.do_listen:
            print("Listen: Stopping service ...")
            self._stop.set()
            self._server_thread.join(timeout=0)
            self.do_listen = False
            self._server_socket.close()
            print("Listen: Stopped")

        else:
            print("Listener: Service wasn't running. Nothing to stop.")

    def _listen_for_broadcasts(self):
        while not self._stop.is_set():
            print("listen")
            message, address = self._server_socket.recvfrom(512)
            self.message_callback_func(message.decode(), address)
            print('message (%s) from : %s' % (str(message), address[0]))

