
import sys
import time
import datetime

import config
import iptables
import arp


if __name__ == '__main__':

    iptables.cleanup_counter()
    iptables.init_counter()

    for node in config.nodes:
        print('Adding pre-configured node:' + node)
        iptables.add_counter(node)

    for addr in arp.addresses():
        if addr not in config.nodes:
            print('Adding un-named node:' + addr)
            iptables.add_counter(addr)

    while True:
        print(datetime.datetime.utcnow().strftime('%H:%M:%S ')),
        print iptables.read_counters()
        sys.stdout.flush()
        time.sleep(config.update_seconds)  # TODO: use timer for accuracy
