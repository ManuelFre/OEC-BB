import subprocess
import ipaddress
import threading
import socket
import os
import broadcast



DEFAULT_APPLICATION_PORT = 48881
RASPBERRY_WIFI_INTERFACE = "wlan0"


class Com(object):
    def __init__(self, port=DEFAULT_SERVER_PORT):
        self.port = port

        self._server_thread = None
        self._server_socket = None

        self._client_threads = []  # formally threads = []

    def start_server(self):
        self._bind_port()
        # TODO: mach was mit anfragen

    def _bind_port(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self._server_socket.bind(('', self.port))
            

    def start_client_search(self):
        print('Start listening service ...')
        self._server_thread = threading.Thread(target=self._listen_for_broadcasts)
        self._server_thread.start()

    def stop_client_search(self):
        self._server_thread.join()


    def _listen_for_broadcasts(self):
        t = getattr(self, "_server_thread")
        while getattr(t, "do_run", True):
            message , address = my_socket.recvfrom(512)
            print('message (%s) from : %s' % ( str(message), address[0]))





