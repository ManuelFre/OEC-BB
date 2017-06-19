#!/usr/bin/env python3
import time

from Communication.listen import MessageRCV
from Communication.broadcast import SubnetBroadcaster
from GUI.gui import MainWindow
from MasterElection.default import hold_master_election
from Config.settings import *

rcv = None
snd = None
window = None
know_network_nodes = []


def main():
    global rcv
    global snd
    global window
    snd = SubnetBroadcaster(DEFAULT_APPLICATION_PORT, GOODBYE_MSG)
    rcv = MessageRCV(process_incoming_message, DEFAULT_APPLICATION_PORT)
    window = MainWindow(listener_start_callback=rcv.start_listening, listener_stop_callback=rcv.stop_listening, app_close_callback=handle_app_close_cmd)
    
    window.show()


def handle_app_close_cmd():
    print("Trying to shut shit down")
    global rcv
    global snd

    snd.terminate()
    rcv.stop_listening()


def update_known_peers(action, addr):
    if action.lower() == 'add':
        if addr not in know_network_nodes:
            print("Node '{}' joined!".format(addr[0]))
            know_network_nodes.append(addr)

    if action.lower() == 'remove':
        if addr in know_network_nodes:
            print("Node '{}' left!".format(addr[0]))
            know_network_nodes.remove(addr)


def do_peer_ping_sync():
    global snd
    global know_network_nodes
    print('Network Node Sync: Started')

    know_network_nodes = []
    snd.send(SYNC_REQUEST_MSG)
    time.sleep(PEER_SYNC_TIMEOUT)  # give peers 10 secs to resp
    for node in know_network_nodes:
        update_peers_and_inform_gui(node[0], node[1])
    print('Network Node Sync: Finished')


def resp_to_ping_sync():
    global snd
    snd.send(SYNC_AKN_MSG)


def update_peers_and_inform_gui(action, addr):
    global window
    update_known_peers(action, addr)
    master_addr = hold_master_election(know_network_nodes)
    master_ip = master_addr[0]
    node_ips = [node_addr[0] for node_addr in know_network_nodes]
    window.update_window_by_ip_list(node_ips)
    window.update_master(master_ip)


def process_incoming_message(msg, addr):
    global window
    if msg == GOODBYE_MSG:
        update_peers_and_inform_gui('remove', addr)
    else:
        update_peers_and_inform_gui('add', addr)

    if msg == SYNC_REQUEST_MSG:
        resp_to_ping_sync()
    print(','.join([str(e) for e in addr]))
    full_str = msg + ' from: ' + addr[0]
    print(full_str)
    window.make_state_active(full_str)


if __name__ == '__main__':  # execute this if this file is called from cli
    print('Let\'s do this.')
    main()


