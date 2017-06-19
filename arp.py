
import remote


def is_ip(text):
    pieces = text.split('.')
    if len(pieces) != 4:
        return False
    try:
        return all(0 <= int(p) < 256 for p in pieces)
    except ValueError:
        return False


def addresses():
    """Return list of IP,MAC pairs"""
    # normally 'arp -n'
    output = remote.execute('arp show')
    try:
        result = output.splitlines(False)
        lines = [x.split() for x in result if len(x) > 0 and is_ip(x.split()[0])]
        pairs = [(x[0], x[3].upper()) for x in lines]
        return pairs
    except AttributeError:
        return []


if __name__ == '__main__':
    print addresses()
