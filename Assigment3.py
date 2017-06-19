#!/usr/bin/env python3
import time

from Communication.listen import MessageRCV
from Communication.broadcast import SubnetBroadcaster
from GUI.gui import MainWindow
from MasterElection.default import hold_master_election
from Config.settings import *
from Misc.helpers import debug_print
import threading

# TODO:
# schönere art master election zu definieren
# doc
# all constants in init


class App(object):
    def __init__(self):
        self.know_network_nodes = []
        self.peer_sync_interval = PEER_SYNC_INTERVAL
        self.port = DEFAULT_APPLICATION_PORT

    def start(self):
        self.snd = SubnetBroadcaster(self.port, GOODBYE_MSG)
        self.rcv = MessageRCV(self.process_incoming_message, self.port)
        self.window = MainWindow(listener_start_callback=self.start_communication,
                                 listener_stop_callback=self.stop_communication,
                                 app_close_callback=self.stop)
        self.window.show()

    def start_communication(self):
        self.rcv.start_listening()
        # start checking if nodes are still there
        self._ping_peer_thread = threading.Thread(target=self.schedule_peer_ping_sync)
        self._ping_peer_thread.setDaemon(True)
        self._ping_peer_thread.start()

    def stop_communication(self):
        self.rcv.stop_listening()
        if getattr(self, '_ping_peer_thread'):
            self._ping_peer_thread.join()

    def stop(self):
        self.snd.terminate()
        self.rcv.stop_listening()

    def update_known_peers(self, action, addr):
        if action.lower() == 'add':
            if addr not in self.know_network_nodes:
                debug_print("Node '{}' joined!".format(addr[0]))
                self.know_network_nodes.append(addr)

        if action.lower() == 'remove':
            if addr in self.know_network_nodes:
                debug_print("Node '{}' left!".format(addr[0]))
                self.know_network_nodes.remove(addr)

    def schedule_peer_ping_sync(self, interval=None):
        if not interval:
            interval = self.peer_sync_interval

        while True:
            debug_print('Network Node Sync: PRE')
            self.do_peer_ping_sync()
            debug_print('Network Node Sync: Next sync in {} seconds'.format(interval))
            time.sleep(interval)

    def do_peer_ping_sync(self):
        debug_print('Network Node Sync: Started')

        self.know_network_nodes = []
        self.snd.send(SYNC_REQUEST_MSG)
        time.sleep(PEER_SYNC_TIMEOUT)  # give peers 10 secs to resp
        for node in self.know_network_nodes:
            self.update_peers_and_inform_gui(node[0], node[1])
        debug_print('Network Node Sync: Finished')

    def resp_to_ping_sync(self):
        self.snd.send(SYNC_AKN_MSG)

    def update_peers_and_inform_gui(self, action, addr):
        self.update_known_peers(action, addr)
        master_addr = hold_master_election(self.know_network_nodes)
        master_ip = master_addr[0]
        node_ips = [node_addr[0] for node_addr in self.know_network_nodes]
        self.window.update_window_by_ip_list(node_ips)
        self.window.update_master(master_ip)

    def process_incoming_message(self, msg, addr):
        if msg == GOODBYE_MSG:
            self.update_peers_and_inform_gui('remove', addr)
        else:
            self.update_peers_and_inform_gui('add', addr)

        if msg == SYNC_REQUEST_MSG:
            self.resp_to_ping_sync()
        debug_print(','.join([str(e) for e in addr]))
        full_str = msg + ' from: ' + addr[0]
        debug_print(full_str)
        self.window.make_state_active(full_str)


if __name__ == '__main__':  # execute this if this file is called from cli
    debug_print('Let\'s do this.')
    app = App()
    app.start()


