
import logging

import tinydb


class Database:

    def __init__(self):
        self.db = tinydb.TinyDB('db.json')
        self.traffic_table = self.db.table('traffic')

    def add_traffic(self, datetime, address, nbytes, timedelta):
        entry = {'datetime': datetime.isoformat(),
                 'address': address,
                 'bytes': nbytes,
                 'seconds': timedelta.total_seconds()}
        logging.debug(entry)
        self.traffic_table.insert(entry)
