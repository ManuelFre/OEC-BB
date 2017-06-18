import time
from tkinter import *
from tkinter import messagebox
from operator import itemgetter


class MainWindow(object):
    def __init__(self, server_start_callback, client_search_callback, app_close_callback):
        # callback functions 
        self.server_start_callback = server_start_callback
        self.client_search_callback = client_search_callback
        self.app_close_callback = app_close_callback
        self.main_window = self._create_window()

    def _create_window(self):
        main_window = Tk()
        main_window.title("Assignment3")
        main_window.geometry("500x550")
        group = Label(main_window, text="Jahrgang: BWI15",)
        group.pack()
        description = Label(main_window, text="Description: Each device(Pi) in the Network will be listed here!\n"
                                          "If a device (Pi) entry or loss the list will be changed!\n"
                                          "There is also a master election under the devices(Pis)!\n",)
        description.pack()
        self.master = StringVar()
        Label(main_window, textvariable=self.master).pack()
        self.master.set("Master: ")
        self.ip_address_list_box = Listbox(main_window, width=70, height=20)
        self.ip_address_list_box.pack()

        self.startBtn = Button(main_window, text="Start", command=self.client_search_callback)
        self.startBtn.pack()

        self.state = StringVar()
        Label(main_window, textvariable=self.state).pack()
        main_window.protocol("WM_DELETE_WINDOW", self._on_closing)

        return main_window

    def show(self):
        self.main_window.mainloop()

    def _on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.app_close_callback()
            self.main_window.destroy()

    def update_list_box(self, list_of_ip_addresses):
        self.ip_address_list_box.delete(0, END)
        for idx, ip in enumerate(list_of_ip_addresses):
            # TODO: String formatting
            self.ip_address_list_box.insert(END, "Rank " + str(idx) + ":          " + ip)

    def update_master(self, master_ip_addr=None):
        self.master.set("Master: {}".format(master_ip_addr or ''))

    def make_state_active(self, stateMessage, time_to_show=3):
        self.state.set(stateMessage)
        time.sleep(time_to_show)
        self.state.set("")

    def update_window_by_ip_list(self, list_of_peer_ips):

        list_for_sorting = []
        for ip_addr in list_of_peer_ips:
            list_for_sorting.append((int(ip_addr.split('.')[3]), ip_addr))
        list_for_sorting.sort(key=itemgetter(0), reverse=True)
        temp_list = [ip_addr[1] for ip_addr in list_for_sorting]
        self.update_list_box(temp_list[1:])  # skip first element
        self.update_master(temp_list[0])  # first entry only
        # show_state(oldIPAddressesInSubnet, currentIPAddressesInSubnet)  # moved to main
        print("Actuelly list of IPs in the Network: " + str(temp_list))


