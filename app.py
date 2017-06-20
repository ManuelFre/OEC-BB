#!/usr/bin/env python3
import threading
import time

from Communication import helpers
from Communication.broadcast import SubnetBroadcaster
from Communication.listen import MessageRCV
from Communication.peers import NetworkNode
from Config.settings import *
from GUI.gui import MainWindow
from MasterElection.default import hold_master_election
from Misc.helpers import debug_print
from datetime import datetime as dt


class App(object):
    """ This is the app. It combines and orchestrates all other app components. """

    def __init__(self):
        self.know_network_nodes = {}
        self.peer_sync_interval = PEER_SYNC_INTERVAL
        self.peer_sync_active = False
        self.listen_state_on = False
        self.port = DEFAULT_APPLICATION_PORT
        self.own_ip = ''

    def start(self):
        """ Start this app. """
        self.snd = SubnetBroadcaster(self.port, GOODBYE_MSG)
        self.rcv = MessageRCV(self.process_incoming_message, self.port)
        self.window = MainWindow(com_start_callback=self.start_communication,
                                 com_stop_callback=self.stop_communication,
                                 app_close_callback=self.stop)

        own_ip_func = getattr(helpers, GET_OWN_IP_FUNC)  # get the right func dynamically
        self.own_ip = own_ip_func()
        self.know_network_nodes[self.own_ip] = NetworkNode(self.own_ip, DEFAULT_APPLICATION_PORT, banner='*')
        self.window.update_own_ip(self.own_ip)
        self.window.show()

    def stop(self):
        """ Stop this app. """
        self.snd.terminate()
        self.rcv.stop_listening()

    def start_communication(self):
        """ Start listening to and for peers. Start threaded peer sync. """
        if not self.rcv.is_listening:
            self.rcv.start_listening()
            self.peer_sync_active = True
            self._ping_peer_thread = threading.Thread(target=self.schedule_peer_ping_sync)
            self._ping_peer_thread.setDaemon(True)
            self._ping_peer_thread.start()
        else:
            debug_print("Listener: Already running! Nothing started!")

    def stop_communication(self):
        """ Stop listening to and for peers. Stop threaded peer sync. """
        if self.rcv.is_listening:
            self.rcv.stop_listening()
            if getattr(self, '_ping_peer_thread', None):
                self.peer_sync_active = False
                self._ping_peer_thread.join(0)
        else:
            debug_print("Listener: Wasn't running! Nothing stopped!")

    def schedule_peer_ping_sync(self, interval=None):
        """ Run a search for active peers every x seconds.
        Notes: THIS IS A BLOCKING CALL. Use threading.

        Args:
            interval (int): time between syncs in sec. (Default: 'self.peer_sync_interval'.)
        """
        if not interval:
            interval = self.peer_sync_interval

        while self.peer_sync_active:
            self.do_peer_ping_sync()
            debug_print('Network Node Sync: Next sync in {} seconds'.format(interval))
            time.sleep(interval)

    def do_peer_ping_sync(self):
        """ Sends a sync request to peers, sleeps 'PEER_SYNC_TIMEOUT' seconds and then updates the node list.
        Notes: THIS IS A BLOCKING CALL. Use threading.
        """
        debug_print('Network Node Sync: Started')
        self.snd.send(SYNC_REQUEST_MSG)
        timestamp = dt.utcnow()
        time.sleep(PEER_SYNC_TIMEOUT)  # give peers x secs to resp
        # create a list of peers that responded after the timestamp
        peers_alive = [node for node in self.know_network_nodes.values() if node.last_seen > timestamp]
        # create a list of peers that are currently displayed but not online anymore
        peers_offline = [node for node in self.know_network_nodes.values() if node not in peers_alive]
        for node in peers_offline:
            self.update_known_peers_and_inform_gui('remove', (node.ip, node.port))
        debug_print('Network Node Sync: Finished')

    def resp_to_ping_sync(self):
        """ Respond to a peer sync request. """
        self.snd.send(SYNC_AKN_MSG)

    def update_known_peers(self, action, addr):
        """ Updates a peer list by adding/removing the given addr.
        Basic error treatment makes sure that addresses are unique per list.

        Args:
            action: 'add' or 'remove'
            addr (tuple): (ip, port)
        """
        peer_ip = addr[0]
        peer_port = addr[1]

        if peer_ip == self.own_ip:
            return

        if action.lower() == 'add':
            if not self.know_network_nodes.get(peer_ip, None):
                debug_print("Node '{}' joined!".format(peer_ip))
                self.know_network_nodes[peer_ip] = NetworkNode(peer_ip, peer_port)
            else:
                debug_print("Node '{}' was seen!".format(peer_ip))
                self.know_network_nodes[peer_ip].last_seen = dt.utcnow()

        if action.lower() == 'remove':
            if self.know_network_nodes.get(peer_ip, None):
                debug_print("Node '{}' left!".format(peer_ip))
                del self.know_network_nodes[peer_ip]

    def update_known_peers_and_inform_gui(self, action, addr):
        """ Same as 'update_known_peers' but also updates the GUI. """

        self.update_known_peers(action, addr)
        known_node_ips = [node for node in self.know_network_nodes.values()]
        master_node = hold_master_election(known_node_ips)
        self.window.update_window_by_ip_list(known_node_ips)
        self.window.update_master(master_node.ip)

    def process_incoming_message(self, msg, addr):
        """ This function processes all incoming messages and starts the appropriate actions.

        Args:
            msg (str): message
            addr (tuple): (ip, port)
        """
        full_str = msg + ' from: ' + addr[0]
        debug_print('Message rcvd:' + full_str)
        if addr[0] != self.own_ip:
            if msg == GOODBYE_MSG:
                self.update_known_peers_and_inform_gui('remove', addr)
            elif msg == SYNC_AKN_MSG:
                self.update_known_peers_and_inform_gui('add', addr)
            elif msg == SYNC_REQUEST_MSG:
                self.update_known_peers_and_inform_gui('add', addr)
                self.resp_to_ping_sync()
            else:
                self.update_known_peers_and_inform_gui('add', addr)

            self.window.make_state_active(full_str)
        else:
            self.update_known_peers('add', addr)

if __name__ == '__main__':
    """
    This is executed if this file is called from cli.
    """
    debug_print('Let\'s do this.')
    app = App()
    app.start()
