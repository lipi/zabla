
import sys
import time
import datetime
import logging

import config
import iptables
import arp
import database


def bandwidth(num, sec):
    if sec == 0:
        return 0
    return num / sec


def add_users():
    for user, mac in config.users:
        if user not in db.all_users():
            db.add_user(user, mac)


if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    iptables.cleanup_counter()
    iptables.init_counter()
    db = database.Database()

    add_users()

    previous_time = datetime.datetime.utcnow()
    ip_mac = dict(arp.addresses())

    while True:
        counters = iptables.read_counters()
        now = datetime.datetime.utcnow()
        logging.info(counters)

        for address in counters:
            seconds = (now - previous_time).total_seconds()
            num_bytes = counters[address]

            # keep track of usage for logging/monitoring
            db.add_traffic(now, ip_mac[address], num_bytes, seconds)

            # reduce users' credits if they seem to be using the net
            if bandwidth(num_bytes, seconds) > config.bandwidth_limit:
                mac = ip_mac[address]
                db.adjust_seconds(mac=mac, seconds=-seconds)

        previous_time = now

        # refresh our ARP table
        for ip, mac in arp.addresses():
            ip_mac[ip] = mac

        # add any new node to iptables
        for ip in ip_mac:
            if ip not in counters:
                iptables.add_counter(ip)

        time.sleep(config.sampling_interval)
