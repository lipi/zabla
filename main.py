
import sys
import time
import datetime
import logging

import config
import iptables
import arp
import database


if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    iptables.cleanup_counter()
    iptables.init_counter()
    db = database.Database()

    for node in config.nodes:
        logging.info('Adding pre-configured node:' + node)
        iptables.add_counter(node)

    for addr in arp.addresses():
        if addr not in config.nodes:
            logging.info('Adding un-named node:' + addr)
            iptables.add_counter(addr)

    previous_time = datetime.datetime.utcnow()
    while True:
        counters = iptables.read_counters()
        now = datetime.datetime.utcnow()
        logging.info(counters)
        for address in counters:
            db.add_traffic(now, address, counters[address], now - previous_time)
        previous_time = now
        time.sleep(config.update_seconds)
