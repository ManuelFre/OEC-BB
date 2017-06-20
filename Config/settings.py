# This file allows you to control various aspects of how the app operates.


DEFAULT_APPLICATION_PORT = 48881  # default port the application uses
HELLO_MSG = '@hello_sexy_lady@'  # message sent when joining the network (unused)
GOODBYE_MSG = '@quitQ'  # message sent when app leaves network regularly
SYNC_REQUEST_MSG = '@sync'  # message sent a node sync is requested
SYNC_AKN_MSG = SYNC_REQUEST_MSG + '_akn'  # message send when responding to a network sync request
RASPBERRY_WIFI_INTERFACE = "wlan0"  # raspberry's wifi interface name. used depending on GET_OWN_IP_FUNC
MASTERELECTION = 'default'  # determines how a master is elected (pluggable)
GET_OWN_IP_FUNC = 'get_ip_using_standard_if'  # determines how the own ip is derived
PEER_SYNC_TIMEOUT = 10  # give networks x seconds time to respond
PEER_SYNC_INTERVAL = 20  # run a peer update every x seconds
DEBUG_PRINT = True  # print events to console?
