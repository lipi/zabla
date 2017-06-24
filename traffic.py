
import socket
import logging
import datetime

import config
from misc import timestamp


def add_bytes(time, address, nbytes, seconds):
    if 0 == nbytes:
        return  # no point saving an empty entry

    bandwidth = float(nbytes)/seconds
    message = 'internet.bandwidth.{} {} {}'.format(address, int(bandwidth), int(timestamp(time)))
    send(message)


def add_usage(time, user):
    message = 'internet.usage.{} 1 {}'.format(user, int(timestamp(time)))
    send(message)


def add_counter(time, user, counter):
    message = 'internet.counter.{} {} {}'.format(user, counter, int(timestamp(time)))
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
