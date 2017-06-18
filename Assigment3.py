#!/usr/bin/env python3

from Communication.listen import MessageRCV
from Communication.broadcast import SubnetBroadcaster
from GUI.gui import MainWindow

# TODO: Proper master election

# fehlerbehandlung für mehrfach start
# mit try/except auf den socket
# master election dir mit verschiedenen modulen
# wie wird die clientliste gecleant?



DEFAULT_APPLICATION_PORT = 48881
GOODBYE_MSG = '@quit'
RASPBERRY_WIFI_INTERFACE = "wlan0"


rcv = None
snd = None
window = None


def main():
    global rcv
    global snd
    global window
    snd = SubnetBroadcaster(DEFAULT_APPLICATION_PORT, GOODBYE_MSG)
    snd._make_broadcast_socket()
    rcv = MessageRCV(process_incomming_message, DEFAULT_APPLICATION_PORT)
    rcv.start_server()
    window = MainWindow(client_search_callback=rcv.start_listening, server_start_callback=None, app_close_callback=handle_app_close_cmd)
    
    window.show()


# determenig what to display and why shut not be part of the gui. it shut happen here
# def show_state(oldIPAddressesInSubnet, currentIPAddressesInSubnet):
#     stateMessage = ""
#     if len(oldIPAddressesInSubnet) == 0 and len(currentIPAddressesInSubnet) > 0:
#         stateMessage += "One or more devices(Pi's) associated to the Network!\n"
#         stateMessage += "New Master is elected!"
#     else:
#         if len(oldIPAddressesInSubnet) < len(currentIPAddressesInSubnet):
#             stateMessage += "One or more devices(Pi's) associated to the Network!\n"
#         if len(oldIPAddressesInSubnet) > len(currentIPAddressesInSubnet):
#             stateMessage += "One or more devices(Pi's) exit the Network!\n"
#         if len(oldIPAddressesInSubnet) != 0 and len(currentIPAddressesInSubnet) != 0 and oldIPAddressesInSubnet[0] != currentIPAddressesInSubnet[0]:
#             stateMessage += "New Master is elected!"
#     threading.Thread(target=make_state_active, args=(stateMessage,)).start()


def handle_app_close_cmd():
    print("Trying to shut shit down")
    global rcv
    global snd
    rcv.stop_listening()
    snd.sent_goodbye_msg()
    snd._destroy_broadcast_socket()
    rcv.stop_server()


def process_incomming_message(msg, addr):
    full_str = msg + ' from: ' + addr[0]
    print(full_str)
    window.make_state_active(full_str)


if __name__ == '__main__':  # execute this if this file is called from cli
    print('Let\'s do this.')
    main()
    global rcv
    print(rcv._server_thread.isAlive())


