import time
from tkinter import *
from tkinter import messagebox


class MainWindow(object):
    def __init__(self, listener_start_callback, listener_stop_callback, app_close_callback):
        # callback functions 
        self.listener_start_callback = listener_start_callback
        self.listener_stop_callback = listener_stop_callback
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

        self.startBtn = Button(main_window, text="Start Listener", command=self.listener_start_callback)
        self.startBtn.pack()

        self.stopBtn = Button(main_window, text="Stop Listener", command=self.listener_stop_callback)
        self.stopBtn.pack()

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
            self.ip_address_list_box.insert(END, "Node {}:          {}".format(idx, ip))

    def update_master(self, master_ip_addr=None):
        self.master.set("Master: {}".format(master_ip_addr or ''))

    def make_state_active(self, stateMessage, time_to_show=3):
        self.state.set(stateMessage)
        time.sleep(time_to_show)
        self.state.set("")

    def update_window_by_ip_list(self, list_of_peer_ips):
        self.update_list_box(list_of_peer_ips)


