import time
from tkinter import *

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




startBtn = Button(fenster, text="Start", command=start_program)
startBtn.pack()

state = StringVar()
Label(fenster, textvariable=state).pack()

mainloop()
