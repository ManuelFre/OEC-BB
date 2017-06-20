import re
from Misc.helpers import debug_print
from Communication.peers import NetworkNode


def hold_master_election(network_nodes):
    """ This is the default master election algorithm.
    The network_node with the 'lowest ip' will be considered master.

    Args:
        network_nodes (list of NetworkNode): network nodes

    Returns (NetworkNode): master node
    """
    if not network_nodes:
        return NetworkNode('', 0)

    lowest_addr = NetworkNode('999.999.999.999', 999999)
    debug_print("Electing master amongst the following peers:")
    debug_print('['+', '.join([n.ip for n in network_nodes])+']')
    for node in network_nodes:
        if ip_to_int(node.ip) < ip_to_int(lowest_addr.ip):
            lowest_addr = node
    return lowest_addr


# helper funcs
def ip_to_int(ip):
    """ Cast ip string to int """
    ip_int = re.sub('\.', '', ip)
    return int(ip_int)
