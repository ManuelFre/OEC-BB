#!/usr/bin/env python3
import subprocess
import ipaddress
import threading
from operator import itemgetter
import time
from tkinter import *
import socket

# This Code is Created by Roman Zachner

currentIPAddressesInSubnet = []
threads = []

# Create the GUI
fenster = Tk()
fenster.title("Assignment3")
fenster.geometry("500x550")
group = Label(fenster, text="Group: Bind Gerald, Leibrecht Markus, Zachner Roman",)
group.pack()
description = Label(fenster, text="Description: Each device(Pi) in the Network will be listed here!\n"
                                  "If a device(Pi) entry or loss the list will be changed!\n"
                                  "There is also a master election under the devices(Pi's)!\n"
                                  "Communication exists throw Network Ping's!\n",)
description.pack()
master = StringVar()
Label(fenster, textvariable=master).pack()
master.set("Master: ")
ipAddressListbox = Listbox(fenster, width=70, height=20)
ipAddressListbox.pack()



def update_list_box():
    ipAddressListbox.delete(0, END)
    i = 0
    for ip in currentIPAddressesInSubnet:
        if i > 0:
            ipAddressListbox.insert(END, "Rank " + str(i) + ":          " + ip)
        i += 1


def update_master():
    master.set("Master: ")
    if currentIPAddressesInSubnet.__len__() >= 1:
        master.set("Master: " + currentIPAddressesInSubnet[0])


def make_state_active(stateMessage):
    state.set(stateMessage)
    time.sleep(3)
    state.set("")


def show_state(oldIPAddressesInSubnet, currentIPAddressesInSubnet):
    stateMessage = ""
    if len(oldIPAddressesInSubnet) == 0 and len(currentIPAddressesInSubnet) > 0:
        stateMessage += "One or more devices(Pi's) associated to the Network!\n"
        stateMessage += "New Master is elected!"
    else:
        if len(oldIPAddressesInSubnet) < len(currentIPAddressesInSubnet):
            stateMessage += "One or more devices(Pi's) associated to the Network!\n"
        if len(oldIPAddressesInSubnet) > len(currentIPAddressesInSubnet):
            stateMessage += "One or more devices(Pi's) exit the Network!\n"
        if len(oldIPAddressesInSubnet) != 0 and len(currentIPAddressesInSubnet) != 0 and oldIPAddressesInSubnet[0] != currentIPAddressesInSubnet[0]:
            stateMessage += "New Master is elected!"
    threading.Thread(target=make_state_active, args=(stateMessage,)).start()

# Create the network
ip_net = ipaddress.ip_network("192.168.0.0/24")

# Get all hosts on that network
all_hosts = list(ip_net.hosts())

# Split Pings into threads
def split_work(start, stop):
    for i in range(start, stop):
        output = subprocess.Popen(['ping', '-c', '2', '-w', '1', str(all_hosts[i])], stdout=subprocess.PIPE).communicate()    
        if output[0].decode("utf-8").find("64 bytes from") > 0:
            currentIPAddressesInSubnet.append(str(all_hosts[i]))


# For each IP address in the subnet, run the ping command
def program():

    # Start a Server

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 9000))
    sock.listen(100000)

    # Start a Server

    while True:
        global currentIPAddressesInSubnet
        oldIPAddressesInSubnet = currentIPAddressesInSubnet
        currentIPAddressesInSubnet = []
        for n in range(0, len(all_hosts), 5):
            stop = n + 5 if n + 5 <= len(all_hosts) else len(all_hosts)
            t = threading.Thread(target=split_work, args=(n, stop))
            threads.append(t)
            t.start()
        for thread in threads:
            thread.join()

        # Check if Server exists

        rasperryIPsInSubnet = []
        for ip in currentIPAddressesInSubnet:
            try:
                cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                cli_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                cli_sock.connect((ip, 9000))
                rasperryIPsInSubnet.append(ip)
                cli_sock.shutdown(socket.SHUT_RDWR)
                cli_sock.close()
            except Exception:
                cli_sock.close()
        currentIPAddressesInSubnet = rasperryIPsInSubnet

        # Check if Server exists

        list_for_sorting = []
        for ip in currentIPAddressesInSubnet:
            list_for_sorting.append((int(ip.split('.')[3]), ip))
        list_for_sorting.sort(key=itemgetter(0), reverse=True)
        currentIPAddressesInSubnet.clear()
        for ip in list_for_sorting:
            currentIPAddressesInSubnet.append(ip[1])
        update_list_box()
        update_master()
        show_state(oldIPAddressesInSubnet, currentIPAddressesInSubnet)
        print("Actuelly list of IPs in the Network: " + str(currentIPAddressesInSubnet))


def start_program():
    threading.Thread(target=program).start()


startBtn = Button(fenster, text="Start", command=start_program)
startBtn.pack()

state = StringVar()
Label(fenster, textvariable=state).pack()

mainloop()
