
import time
import datetime
import logging

import config
import iptables
import arp
import database
import traffic
from misc import timestamp


def bandwidth(num, sec):
    if sec == 0:
        return 0
    return num / sec


def wait_for_next(period):
    ts = timestamp(datetime.datetime.utcnow())
    time.sleep(period - (ts % period))


if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG)

    iptables.cleanup_counter()
    iptables.init_counter()
    db = database.Database()
    for user, device, mac in config.devices:
        db.add_device(user, device, mac.upper())

    previous_time = datetime.datetime.utcnow()

    ip_mac = dict(arp.addresses())

    while True:
        wait_for_next(config.sampling_interval)
        now = datetime.datetime.utcnow()

        counters = iptables.read_counters()
        logging.info(counters)

        for address in counters:
            seconds = (now - previous_time).total_seconds()
            num_bytes = counters[address]
            mac = ip_mac[address]

            # keep track of usage for logging/monitoring
            # (might want to use previous_time)
            traffic.add_bytes(now, mac, num_bytes, seconds)

            # reduce users' credits if they seem to be using the net
            if bandwidth(num_bytes, seconds) > config.bandwidth_limit:
                user = db.user_of(mac)
                if user:
                    db.add_seconds(user=user, seconds=-seconds)

                    # TODO: add all at once using pickle interface to reduce traffic
                    traffic.add_counter(now, user, counter=int(db.get_seconds(user)))
                    traffic.add_usage(now, user)

        previous_time = now

        # refresh our ARP table
        for ip, mac in arp.addresses():
            ip_mac[ip] = mac

        # add any new node to iptables
        for ip in ip_mac:
            if ip not in counters:
                iptables.add_counter(ip)

