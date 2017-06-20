#!/usr/bin/env python3
import time

from Communication.listen import MessageRCV
from Communication.broadcast import SubnetBroadcaster
from Communication import helpers
from GUI.gui import MainWindow
from MasterElection.default import hold_master_election
from Config.settings import *
from Misc.helpers import debug_print
import threading

# TODO:
# all constants in init


class App(object):
    """ This is the app. It combines and orchistrates all other app components. """
    def __init__(self):
        self.know_network_nodes = []
        self.peer_sync_node_buffer = []
        self.peer_sync_interval = PEER_SYNC_INTERVAL
        self.peer_sync_active = False
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
        self.window.update_own_ip(self.own_ip)
        self.window.show()

    def stop(self):
        """ Stop this app. """
        self.snd.terminate()
        self.rcv.stop_listening()

    def start_communication(self):
        """ Start listening to and for peers. Start threaded peer sync. """
        self.rcv.start_listening()
        # start checking if nodes are still there
        self.peer_sync_active = True
        self._ping_peer_thread = threading.Thread(target=self.schedule_peer_ping_sync)
        self._ping_peer_thread.setDaemon(True)
        self._ping_peer_thread.start()

    def stop_communication(self):
        """ Stop listening to and for peers. Stop threaded peer sync. """
        self.rcv.stop_listening()
        if getattr(self, '_ping_peer_thread', None):
            self.peer_sync_active = False
            self._ping_peer_thread.join(0)

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
        self.peer_sync_node_buffer = []
        self.snd.send(SYNC_REQUEST_MSG)
        time.sleep(PEER_SYNC_TIMEOUT)  # give peers 10 secs to resp
        self.know_network_nodes = []
        for node in self.peer_sync_node_buffer:
            self.update_known_peers_and_inform_gui('add', node)
        debug_print('Network Node Sync: Finished')

    def resp_to_ping_sync(self):
        """ Respond to a peer sync request. """
        self.snd.send(SYNC_AKN_MSG)

    def update_known_peers(self, action, addr, node_list_used=None):
        """ Updates a peer list by adding/removing the given addr.
        Basic error treatment makes sure that addresses are unique per list.

        Args:
            action: 'add' or 'remove'
            addr (tuple): (ip, port)
            node_list_used (list_pointer): switch used to determin which list is updated
        """
        if node_list_used is None:
            node_list_used = self.know_network_nodes

        if action.lower() == 'add':
            if addr not in node_list_used:
                debug_print("Node '{}' joined!".format(addr[0]))
                node_list_used.append(addr)

        if action.lower() == 'remove':
            if addr in node_list_used:
                debug_print("Node '{}' left!".format(addr[0]))
                node_list_used.remove(addr)

    def update_known_peers_and_inform_gui(self, action, addr, node_list_used=None):
        """ Same as 'update_known_peers' but also updates the GUI. """
        if node_list_used is None:
            node_list_used = self.know_network_nodes

        self.update_known_peers(action, addr, node_list_used)
        master_addr = hold_master_election(node_list_used)
        master_ip = master_addr[0]
        node_ips = [node_addr[0] for node_addr in node_list_used]
        self.window.update_window_by_ip_list(node_ips)
        self.window.update_master(master_ip)

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
                self.update_known_peers('add', addr, node_list_used=self.peer_sync_node_buffer)
            elif msg == SYNC_REQUEST_MSG:
                self.resp_to_ping_sync()
            else:
                self.update_known_peers_and_inform_gui('add', addr)

            self.window.make_state_active(full_str)


if __name__ == '__main__':
    """
    This is executed if this file is called from cli.
    """
    debug_print('Let\'s do this.')
    app = App()
    app.start()


