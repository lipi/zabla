
import datetime
import time
import logging

import remote


def list_rules():
    return remote.execute('iptables -L COUNTER')


def cleanup_counter():
    logging.debug('cleaning up existing counters...')
    remote.execute('iptables -F COUNTER')
    rules = list_rules()
    while ('0 references' not in rules) and ('No chain' not in rules):  # left behind by previous runs
        rules = list_rules()
        remote.execute('iptables -D FORWARD -j COUNTER')


def init_counter():
    logging.debug('initializing counter...')
    remote.execute('iptables -N COUNTER; iptables -I FORWARD -j COUNTER')


def add_counter(address):
    remote.execute('iptables -A COUNTER --dst ' + address)


def read_counters(tries=3):
    """Returns dictionary of IP address keys and data usage values"""
    response = None
    while not response and tries > 0:
        response = remote.execute('iptables -L COUNTER -vx; iptables -Z COUNTER')
    lines = [x for x in response.splitlines(False) if 'anywhere' in x]
    counters = {}
    for line in lines:
        address = line.split()[-1]
        counter = line.split()[1]  # bytes
        counters[address] = int(counter)
    return counters


if __name__ == '__main__':
    cleanup_counter()
    init_counter()
    add_counter('192.168.1.2')
    add_counter('192.168.1.3')
    add_counter('192.168.1.4')

    while True:
        print(datetime.datetime.utcnow().strftime('%H:%M:%S ')),
        print read_counters()
        time.sleep(2)
