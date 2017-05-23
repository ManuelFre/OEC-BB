#!/usr/bin/env python3

from Communication.networking import Com
from GUI.gui import MainWindow

# TODO: Proper master election


def main():
    com = Com()
    com.start_server()
    com.start_client_search()
    window = MainWindow(client_search_func=com.start_client_search, server_start_func=None)
    window.show()

# determenig what to display and why shut not be part of the gui. it shut happen here
# def show_state(oldIPAddressesInSubnet, currentIPAddressesInSubnet):
#     stateMessage = ""
#     if len(oldIPAddressesInSubnet) == 0 and len(currentIPAddressesInSubnet) > 0:
#         stateMessage += "One or more devices(Pi's) associated to the Network!\n"
#         stateMessage += "New Master is elected!"
#     else:
#         if len(oldIPAddressesInSubnet) < len(currentIPAddressesInSubnet):
#             stateMessage += "One or more devices(Pi's) associated to the Network!\n"
#         if len(oldIPAddressesInSubnet) > len(currentIPAddressesInSubnet):
#             stateMessage += "One or more devices(Pi's) exit the Network!\n"
#         if len(oldIPAddressesInSubnet) != 0 and len(currentIPAddressesInSubnet) != 0 and oldIPAddressesInSubnet[0] != currentIPAddressesInSubnet[0]:
#             stateMessage += "New Master is elected!"
#     threading.Thread(target=make_state_active, args=(stateMessage,)).start()

if __name__ == '__main__':  # execute this if this file is called by a cli
    print('Let\'s do this.')
    main()

