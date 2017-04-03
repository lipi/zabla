
import datetime

import matplotlib.pyplot as plt
import matplotlib.pyplot as mpld3


def plot(traffic):
    data = [(datetime.datetime.utcfromtimestamp(x['timestamp']),
             x['bytes']/x['seconds']/1000.0,
             x['seconds'] / (24 * 3600.))
            for x in traffic]
    for d, b, w in data:
        print d, b, w
    dates, values, width = zip(*data)
    fig, ax = plt.subplots()
    ax.set_ylabel('Bandwidth [kbytes/sec]')
    ax.set_alpha(0.5)
    ax.grid(True)
    shifted_width = list(width[1:]) + [width[-1]]

    plt.xticks(rotation=90)
    ax.set_yscale('log')
    ax.xaxis_date()
    ax.bar(dates, values, width=shifted_width)
    plt.show()
    #mpld3.show()


if __name__ == '__main__':
    import database
    db = database.Database()
    tr = db.get_traffic('192.168.1.2')
    plot(tr)

