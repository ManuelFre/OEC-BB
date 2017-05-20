import subprocess
import ipaddress
import threading
import socket


DEFAULT_SERVER_PORT = 9000
RASPBERRY_WIFI_INTERFACE = "wlan0"


class Com(object):
    def __init__(self, port=DEFAULT_SERVER_PORT):
        self.port = port

        self.ip_net = ipaddress.ip_network("192.168.0.0/24")  # TODO: Make dynamic: see http://stackoverflow.com/a/936536
        self.all_hosts = list(self.ip_net.hosts()) # Get all potential hosts on that network
        self.live_hosts = []  # we don't know jet which host are alive
        self.peer_hosts = []  # we don't know jet which host are running the same software

        self._server_thread = None

        self._client_threads = []  # formally threads = []

    def start_server(self):
        self._bind_port()
        # TODO: mach was mit anfragen

    def _bind_port(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('', self.port))
        sock.listen(5)

    def start_client_search(self):
        self._server_thread = threading.Thread(target=self._monitor_current_subnet_for_peers)
        self._server_thread.start()

    def stop_client_search(self):
        self._server_thread.join()

    def _ping_subnet(self):

        # TODO umschreiben, dass nicht immer die ganze liste gelösht und wieder befüllt werden muss
        # Immer einen host nach dem anderen updaten und dessen state ändern oder so
        self.live_hosts = []
        for n in range(0, len(self.all_hosts), 5):
            stop = n + 5 if n + 5 <= len(self.all_hosts) else len(self.all_hosts)
            t = threading.Thread(target=self.ping_hosts, args=(n, stop))
            self._client_threads.append(t)
            t.start()
        for thread in self._client_threads:
            thread.join()

    def ping_hosts(self, start, stop):
        """
        Pings the ip addresses in the sequence from :param start to :param stop and
         adds all live hosts to self.live_hosts
        :param start: lower sequence limiter
        :param stop: upper sequence limiter
        """
        for i in range(start, stop):

            # TODO: Das muss schöner werden! subprocess verursacht krebs
            output = subprocess.Popen(['ping', '-n', '1', '-w', '500', str(self.all_hosts[i])],
                                      stdout=subprocess.PIPE, startupinfo=None).communicate()[0]
            if "Empfangen = 1" in output.decode('gb2312', errors='ignore'):
                self.live_hosts.append(str(self.all_hosts[i]))

    def _try_handshake(self):
        for ip_addr in self.live_hosts:
            try:
                cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                cli_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                cli_sock.connect((ip_addr, self.port))
                # TODO: hier muss eine echte Komm mit dem Server stattfinden
                # nur so kann man sich sicher sein, dass nicht nur zufällig der Port offen ist
                self.peer_hosts.append(ip_addr)
                cli_sock.shutdown(socket.SHUT_RDWR)
                cli_sock.close()
            except Exception as exc:
                print(exc)

    def _monitor_current_subnet_for_peers(self):
        while True:
            self._ping_subnet()
            self._try_handshake()





