#!/usr/bin/env python3

from Communication.listen import MessageRCV
from Communication.broadcast import SubnetBroadcaster
from GUI.gui import MainWindow
from MasterElection.default import hold_master_election

# TODO: Proper master election

# fehlerbehandlung für mehrfach start
# mit try/except auf den socket
# master election dir mit verschiedenen modulen
# wie wird die clientliste gecleant?



DEFAULT_APPLICATION_PORT = 48881
HELLO_MSG = '@hello_sexy_lady@'
GOODBYE_MSG = '@quit'
RASPBERRY_WIFI_INTERFACE = "wlan0"
MASTERELECTION = 'default'


rcv = None
snd = None
window = None
know_network_nodes = []


def main():
    global rcv
    global snd
    global window
    snd = SubnetBroadcaster(DEFAULT_APPLICATION_PORT, GOODBYE_MSG)
    snd._make_broadcast_socket()
    rcv = MessageRCV(process_incomming_message, DEFAULT_APPLICATION_PORT)
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


    snd.send_goodbye_msg()
    snd._destroy_broadcast_socket()
    rcv.stop_listening()


def update_peers(action, addr):
    ip, port = addr
    print('known:')
    print(know_network_nodes)
    if action.lower() == 'add':
        if addr not in know_network_nodes:
            print("Node '{}' joined!".format(addr[0]))
            know_network_nodes.append(addr)

    if action.lower() == 'remove':
        if addr in know_network_nodes:
            print("Node '{}' left!".format(addr[0]))
            know_network_nodes.remove(addr)


def update_peers_and_inform_gui(action, addr):
    global window
    update_peers(action, addr)
    master_addr = hold_master_election(know_network_nodes)
    master_ip = master_addr[0]
    node_ips = [node_addr[0] for node_addr in know_network_nodes]
    window.update_window_by_ip_list(node_ips)
    window.update_master(master_ip)



def process_incomming_message(msg, addr):
    global window
    if msg != GOODBYE_MSG:
        update_peers_and_inform_gui('add', addr)
    else:
        update_peers_and_inform_gui('remove', addr)

    print(','.join([str(e) for e in addr]))
    full_str = msg + ' from: ' + addr[0]
    print(full_str)
    window.make_state_active(full_str)



if __name__ == '__main__':  # execute this if this file is called from cli
    print('Let\'s do this.')
    main()


