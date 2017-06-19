
#
# edit this file as necessary
#

# address of router
host = '192.168.1.1'
port = 23
user = 'admin'
password = '<insert password here>'  # or set it in config_local.py

sampling_interval = 60  # seconds
bandwidth_limit = 1000  # bytes per second
users = [
    ["example", '12:34:56:78:90:ab'],
    ["somebody's phone", 'aa:bb:cc:dd:ee:ff']
]

carbon_server = 'localhost'
carbon_port = 2003

try:
    from config_local import *
except ImportError:
    print('No local config')
    pass
