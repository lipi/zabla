
import telnetlib
import socket
import logging

import config


def _execute(cmd):
    #logging.debug('execute:' + cmd)
    session = telnetlib.Telnet(config.host, config.port, timeout=5.0)

    session.read_until('ogin: ')
    session.write(config.user + '\n')
    session.read_until('assword: ')
    session.write(config.password + '\n')
    session.read_eager()  # flush login prompt

    session.write(cmd + '\n')

    session.write('exit\n')
    response = session.read_all()
    #logging.debug('response:' + response)
    session.close()  # be nice to remote host
    return response


def execute(cmd, tries=3):
    response = None
    while tries > 0 and not response:
        try:
            response = _execute(cmd)
        except socket.timeout:
            #logging.debug('timeout')
            pass
        except EOFError as eof:
            #logging.info(eof)
            break

    return response


if __name__ == '__main__':
    print(execute('iptables -L -vx'))
