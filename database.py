
import os
import logging


# TODO: use thread-safe DB instead of tinydb
import tinydb


class Database:

    def __init__(self):
        try:
            os.mkdir('db')
        except OSError:
            pass
        self.devices = tinydb.TinyDB('db/devices.json')
        self.counters = tinydb.TinyDB('db/counters.json')

    def add_device(self, user, device, mac='00:00:00:00:00:00'):
        query = tinydb.Query()
        row = self.devices.get(query.mac == mac)
        if row:
            self.devices.update({'user': user, 'device': device}, query.mac == mac)
        else:
            self.devices.insert({'user': user, 'device': device, 'mac': mac})

    def all_macs(self):
        return [x['mac'] for x in self.devices.all()]

    def user_of(self, mac):
        query = tinydb.Query()
        row = self.devices.get(query.mac == mac)
        if row:
            user = row['user']
        else:
            user = ''
        return user

    def add_seconds(self, user, seconds):
        logging.debug("Adjusting {}'s time by {} seconds".format(user, seconds))
        current = self.get_seconds(user)
        counter = tinydb.Query()
        eid = self.counters.update({'seconds': current + seconds}, counter.user == user)
        if not eid:
            self.counters.insert({'seconds': seconds, 'user': user})

    def get_seconds(self, user):
        counter = tinydb.Query()
        seconds = 0
        try:
            seconds = self.counters.get(counter.user == user)['seconds']
        except Exception as ex:
            print ex
        return seconds

    def set_seconds(self, user, seconds):
        logging.debug("Resetting {}'s time to {} seconds".format(user, seconds))
        counter = tinydb.Query()
        try:
            self.counters.update({'seconds': seconds}, counter.user == user)
        except Exception as ex:
            print ex


if __name__ == '__main__':
    db = Database()
    db.add_device('testuser', 'testdevice', 'testmac')
    db.add_seconds('testuser', 10)
    print db.get_seconds('testuser')
    db.add_seconds('testuser', 10)
    print db.get_seconds('testuser')
    db.set_seconds('testuser', 0)
    print db.get_seconds('testuser')


