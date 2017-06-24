
import datetime


def timestamp(time):
    return (time - datetime.datetime(1970, 1, 1)).total_seconds()

