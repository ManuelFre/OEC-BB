import socket
import fcntl
import struct
import subprocess
import sys

# as suggested by https://stackoverflow.com/questions/24196932/how-can-i-get-the-ip-address-of-eth0-in-python#24196955
def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s',
                                                                        ifname[:15]))[20:24])



# source: https://sfeole.wordpress.com/2012/09/27/simple-python3-code-to-parse-your-ipaddress/
def get_ip_address_ifconfig(interface):
    myaddress = subprocess.getoutput("/sbin/ifconfig %s" % interface)\
                .split("\n")[1].split()[1][5:]
    myaddress.replace('se:', '')  # can happen depending on os lang
    if myaddress == "CAST":
        print("Please Confirm that your Network Device is Configured")
        sys.exit()
    else:
        return myaddress


# ugly patching
get_ip_address = get_ip_address_ifconfig