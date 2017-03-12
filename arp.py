
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
    # normally 'arp -n'
    lines = remote.execute('arp show').splitlines(False)
    result = [x.split()[0] for x in lines if len(x) > 0 and is_ip(x.split()[0])]
    return result


if __name__ == '__main__':
    print addresses()
