import subprocess
import ipaddress
import threading
import socket
import os


class MessageRCV(object):
    def __init__(self, message_callback_func, port):
        self.port = port

        self._stop = threading.Event()
        self._server_thread = None
        self._server_socket = None

        self.message_callback_func = message_callback_func

        self.do_listen = False

    def start_server(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._server_socket.bind(('', self.port))

    def start_listening(self):
        print('Start listening service ...')
        self.do_listen = True
        self._server_thread = threading.Thread(target=self._listen_for_broadcasts)
        self._server_thread.setDaemon(True)
        self._server_thread.start()

    def stop_listening(self):
        print("stop_listening")
        self._stop.set()
        self._server_thread.join(timeout=0)
        print(self._server_thread.isAlive())
        print("After")

    def stop_server(self):
        print("stop_server")
        self._server_socket.close()

    def _listen_for_broadcasts(self):
        #t = threading.currentThread()
        #while getattr(t, "do_run", True):


        # mit timeout
        while not self._stop.is_set():
            print("listen")
            message, address = self._server_socket.recvfrom(512)
            self.message_callback_func(message.decode(), address)
            print('message (%s) from : %s' % (str(message), address[0]))

