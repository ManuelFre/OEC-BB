import re
from Misc.helpers import debug_print


def hold_master_election(network_nodes):
    """ This is the default master election algorithm.
    The addr with the 'lowest ip' will be considered master.

    Args:
        network_nodes (list of tuples): eg ('192.168.1.4', 23423)

    Returns (tuple): master_address. eg ('192.168.1.4', 23423)
    """
    if not network_nodes:
        return ('', None)

    lowest_addr = ('999.999.999.999', None)
    debug_print("Electing master amongst the following peers:")
    debug_print('['+', '.join([n[0] for n in network_nodes])+']')
    for ip, port in network_nodes:
        if ip_to_int(ip) < ip_to_int(lowest_addr[0]):
            lowest_addr = (ip, port)
    return lowest_addr


# helper funcs
def ip_to_int(ip):
    """ Cast ip string to int """
    ip_int = re.sub('\.', '', ip)
    return int(ip_int)
