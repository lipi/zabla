
import telnetlib
import socket

import config


def _execute(cmd):
    # print('execute:' + cmd)
    session = telnetlib.Telnet(config.host, config.port, timeout=5.0)

    session.read_until('ogin: ')
    session.write(config.user + '\n')
    session.read_until('assword: ')
    session.write(config.password + '\n')
    session.read_eager()  # flush login prompt

    session.write(cmd + '\n')

    session.write('exit\n')
    response = session.read_all()
    session.close()  # be nice to remote host
    return response


def execute(cmd):
    try:
        return _execute(cmd)
    except socket.timeout:
        return ' '  # avoid being None

if __name__ == '__main__':
    print(execute('iptables -L -vx'))
