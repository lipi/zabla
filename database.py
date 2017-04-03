
import logging
import datetime

# TODO: use thread-safe DB instead of tinydb
import tinydb


class Database:

    def __init__(self):
        self.traffic = tinydb.TinyDB('traffic.json')
        self.users = tinydb.TinyDB('users.json')

    def add_traffic(self, time, address, nbytes, seconds):
        if 0 == nbytes:
            return  # no point saving an empty entry
        entry = {'timestamp': int(time.strftime('%s')),  # seconds since Epoch, cheap to compare
                 'address': address,
                 'bytes': nbytes,
                 'seconds': seconds}
        logging.debug(entry)
        self.traffic.insert(entry)

    def get_traffic(self,
                    address,
                    start=datetime.datetime.fromtimestamp(0),
                    end=datetime.datetime.utcnow()):
        start_seconds = start.strftime('%s')
        end_seconds = end.strftime('%s')
        node = tinydb.Query()
        return self.traffic.search((node.address == address) &
                                   (start_seconds <= node.timestamp < end_seconds))

    def add_user(self, name, mac='00:00:00:00:00:00'):
        self.users.insert({'name': name, 'seconds': 0, 'mac': mac})

    def all_users(self):
        return [x['name'] for x in self.users.all()]

    def add_seconds(self, name, seconds):
        current = self.get_seconds(name)
        user = tinydb.Query()
        self.users.update({'seconds': current + seconds}, user.name == name)

    def get_seconds(self, name):
        user = tinydb.Query()
        seconds = 0
        try:
            seconds = self.users.get((user.name == name))['seconds']
        except TypeError:
            pass
        return seconds

    def adjust_seconds(self, mac, seconds):
        logging.debug("Adjusting {}'s time by {} seconds".format(mac, seconds))
        user = tinydb.Query()
        row = self.users.get((user.mac == mac))
        if row:
            self.add_seconds(row['name'], seconds)


if __name__ == '__main__':
    db = Database()
    db.add_user('test')
    db.add_seconds('test', 10)
    print db.get_seconds('test')
    db.add_seconds('test', 10)
    print db.get_seconds('test')



