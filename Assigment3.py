#!/usr/bin/env python3

from Communication import Com
from GUI import *

# This Code is Created by Roman Zachner


def main():
    com = Com()
    com.start_server()
    com.start_client_search()


if __name__ == '__main__':  # execute this if this file is called by a cli
    print('Let\'s do this.')
    main()

