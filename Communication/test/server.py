import socket

def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    my_socket.bind(('',48881))

    print 'start service ...'

    while True :
        message , address = my_socket.recvfrom(512)
        print 'message (%s) from : %s' % ( str(message), address[0])

if __name__ == "__main__" :
    main()
