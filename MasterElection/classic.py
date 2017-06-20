from operator import itemgetter


def hold_master_election(network_nodes):
    """ This is a UNTESTED reconstruction of the original master election algorithm.
    Here for reference only!
    """
    list_for_sorting = []
    for ip_addr, port in network_nodes:
        list_for_sorting.append((int(ip_addr.split('.')[3]), ip_addr))
    list_for_sorting.sort(key=itemgetter(0), reverse=True)
    temp_list = [ip_addr[1] for ip_addr in list_for_sorting]

    return temp_list[0]
