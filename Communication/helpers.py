import socket
import fcntl
import struct
import subprocess
import sys
from Config.settings import RASPBERRY_WIFI_INTERFACE


def get_ip_address_python2(ifname=RASPBERRY_WIFI_INTERFACE):
    """
    Most reliable version to get own ip address given a valid interface name.
    DOESN'T WORK WITH PYTHON 3!

    Source: https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-of-eth0-in-python#24196955

    Args:
        ifname (str): interface name

    Returns (str): own ip address on that interface
    """

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                                                        ifname[:15]))[20:24])


def get_ip_address_ifconfig(ifname=RASPBERRY_WIFI_INTERFACE):
    """
    Parses IP address from ifconfig. This can be a bitch because it might be os lang dependant!

    Source: https://sfeole.wordpress.com/2012/09/27/simple-python3-code-to-parse-your-ipaddress/
    Args:
        ifname (str): interface name

    Returns: own ip address on that interface
    """
    myaddress = subprocess.getoutput("/sbin/ifconfig %s" % interface)\
                .split("\n")[1].split()[1][5:]
    myaddress = myaddress.replace('se:', '')  # can happen depending on os lang
    if myaddress == "CAST":
        print("Please Confirm that your Network Device is Configured")
        sys.exit()
    else:
        return myaddress


def get_ip_using_standard_if(host='8.8.8.8'):
    """
    Gets the ip of the 'standard interface'

    Source: https://stackoverflow.com/a/7335145
    Args:
        host (str): optional ip of a host to connect to. Default is '8.8.8.8'

    Returns: own ip address on standard interface
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        s.connect((host, 9))
        client = s.getsockname()[0]
    except socket.error:
        client = "Unknown IP"
    finally:
        del s
    return client
