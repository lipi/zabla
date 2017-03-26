
#
# edit this file as necessary
#

# address of router
host = '192.168.1.1'
port = 23
user = 'admin'
password = '<insert password here>'  # or set it in config_local.py

update_seconds = 60

# this assumes fixed IP addresses, i.e. static DHCP leases
nodes = {
    '192.168.1.2': "His laptop",
    '192.168.1.3': "Her laptop",
    '192.168.1.4': "Chromecast",
    '192.168.1.5': "Her phone",
}

try:
    from config_local import *
except ImportError:
    print('No local config')
    pass
