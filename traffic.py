
import socket
import logging
import datetime

import config


def timestamp(time):
    return int((time - datetime.datetime(1970, 1, 1)).total_seconds())


def add_bytes(time, address, nbytes, seconds):
    if 0 == nbytes:
        return  # no point saving an empty entry

    bandwidth = float(nbytes)/seconds
    message = 'internet.bandwidth.{} {} {}'.format(address, int(bandwidth), timestamp(time))
    send(message)
    if bandwidth > config.bandwidth_limit:
        add_usage(time, address)


def add_usage(time, address):
    message = 'internet.usage.{} 1 {}'.format(address, timestamp(time))
    send(message)


def add_counter(time, user, counter):
    message = 'internet.counter.{} {} {}'.format(user, counter, timestamp(time))
    send(message)


def send(message):
    logging.debug('sending message:' + message)
    sock = socket.socket()
    sock.connect((config.carbon_server, config.carbon_port))
    sock.sendall(message + '\n')
    sock.close()

if __name__ == '__main__':
    add_bytes(datetime.datetime.now(), 'ff', 1000, 10)
    add_bytes(datetime.datetime.now(), '55', 10000, 10)
