import re
from Misc.helpers import debug_print


def hold_master_election(network_nodes):
    """
    This is the default master election algorithm.
    The addr with the 'lowest ip' will be considered master.

    :param network_nodes (list of tuples): eg ('192.168.1.4', 23423)
    :return master_address: ('192.168.1.4', 23423)
    """

    if not network_nodes:
        return ('', None)

    lowest_addr = ('999.999.999.999', None)
    print(network_nodes)
    for ip, port in network_nodes:
        print(ip, lowest_addr[0], ip_to_int(ip), ip_to_int(lowest_addr[0]), ip_to_int(ip) < ip_to_int(lowest_addr[0]))
        if ip_to_int(ip) < ip_to_int(lowest_addr[0]):
            lowest_addr = (ip, port)
            print('lowest ip now: {}'.format(lowest_addr[0]))
    return lowest_addr


# helper funcs
def ip_to_int(ip):
    ip_int = re.sub('\.', '', ip)
    print(ip_int)
    return int(ip_int)
