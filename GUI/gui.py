import time
from tkinter import *
from tkinter import messagebox


class MainWindow(object):
    """ This class contains the apps GUI and it's behavior.

    Args:
        com_start_callback (func_pointer): function to call when 'Start Com' is clicked.
        com_stop_callback (func_pointer): function to call when 'Stop Com' is clicked.
        app_close_callback (func_pointer): function to call when the app gets closes regularly.
    """

    def __init__(self, com_start_callback, com_stop_callback, app_close_callback):
        # callback functions 
        self.com_start_callback = com_start_callback
        self.com_stop_callback = com_stop_callback
        self.app_close_callback = app_close_callback
        self.main_window = self._create_window()

    def _create_window(self):
        """ Internal function to create windown and store it in RAM.

        Returns: GUI window
        """
        main_window = Tk()
        main_window.title("Assignment3")
        main_window.geometry("500x550")
        group = Label(main_window, text="Jahrgang: BWI15-BB",)
        group.pack()
        description = Label(main_window, text="Description: Each device(Pi) in the Network will be listed here!\n"
                                          "If a device (Pi) entry or loss the list will be changed!\n"
                                          "There is also a master election under the devices(Pis)!\n",)
        description.pack()
        self.master = StringVar()
        Label(main_window, textvariable=self.master).pack()
        self.master.set("Master: ")

        self.own_ip = StringVar()
        Label(main_window, textvariable=self.own_ip).pack()
        self.own_ip.set("Own IP: ")

        self.ip_address_list_box = Listbox(main_window, width=70, height=20)
        self.ip_address_list_box.pack()

        self.startBtn = Button(main_window, text="Start Com", command=self.com_start_callback)
        self.startBtn.pack()

        self.stopBtn = Button(main_window, text="Stop Com", command=self.com_stop_callback)
        self.stopBtn.pack()

        self.state = StringVar()
        Label(main_window, textvariable=self.state).pack()
        main_window.protocol("WM_DELETE_WINDOW", self._on_closing)

        return main_window

    def show(self):
        """ Make window visible. """
        self.main_window.mainloop()

    def _on_closing(self):
        """ Internal function that creates a 'do you really want to quit?' popup and then closes the app. """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.app_close_callback()
            self.main_window.destroy()

    def update_window_by_ip_list(self, nodes):
        """ Takes a list of ips and shows displays them on the window.
        Args:
            nodes (list of NetworkNode): ip addresses
        """

        self.ip_address_list_box.delete(0, END)
        for idx, node in enumerate(nodes):
            self.ip_address_list_box.insert(END, "Node {idx:02d}:{n.ip: >16}:{n.port} {n.banner}".format(idx=idx, n=node))

    def update_master(self, master_ip_addr=None):
        """ Displays a given ip as master. Empty param. can be used to reset it.

        Args:
            master_ip_addr (str): IP that will be displayed
        """
        self.master.set("Master: {}".format(master_ip_addr or ''))

    def update_own_ip(self, ip_addr=None):
        """ Displays a given ip as own ip. Empty param. can be used to reset it.

        Args:
            ip_addr (str): IP that will be displayed
        """
        self.own_ip.set("Own IP: {}".format(ip_addr or ''))

    def make_state_active(self, stateMessage, time_to_show=1):
        """ Flashes a message for a given time (default: 1s).
        Notes: THIS IS A BLOCKING CALL!

        Args:
            stateMessage (str): message to display
            time_to_show (int): show duration in sec. (default: 1)
        """
        self.state.set(stateMessage)
        time.sleep(time_to_show)
        self.state.set("")


