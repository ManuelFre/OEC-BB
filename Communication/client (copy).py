import socket 
import errno

DEFAULT_BUFFER_SIZE = 1024
CLIENT_AUTH_MESSAGE = 'Hello, world'

# exit codes:
# 0: all good => host is pi server
# 1: port open but wrong / no answer
# 2: connection refused
# 3: other error


class Client(object):
	def __init__(self, buffer_size=None, auth_message=None):
		self.buffer_size = buffer_size or DEFAULT_BUFFER_SIZE
		self.auth_message = auth_message or CLIENT_AUTH_MESSAGE

	def test_connection(self, host, port):
		sock =  socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((host, port))
		sock.sendall(bytes(self.auth_message, 'ascii'))
		response = str(sock.recv(1024), 'ascii')
		socket.close()
		return response

	def check_host(self, host, port):
		try:
			resp = self.test_connection(host, port)
			if self._check_response(resp):
				return 0
			return 1

		except socket.error as exc:
			if exc.errno == errno.ECONNREFUSED:
				return 2
			return 3

	def _check_response(self, response):
		if response == self.auth_message[::-1]:
			return True
		return False
c = Client()
print(c.check_host('localhost', 60000))