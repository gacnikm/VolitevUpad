import os

from peewee import fn
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize

from db import db, Tweet
from racuni import accounts, important

PATH = os.path.dirname(os.path.abspath(__file__))
db.init(os.path.join(PATH, 'db.sqlite'))
db.connect()
db.create_tables([Tweet])

plt.tight_layout()

fig = plt.figure(figsize=(10,len(accounts.items())*4))

plots = len(accounts.items())

for i, (acc, val) in enumerate(accounts.items()):
    ax1 = fig.add_subplot(plots,1,i+1)

    ax1.set_xlabel("Tedni")
    ax1.set_ylabel("Tvitov/teden")

    data = []
    prev_week = 1
    for week, count in Tweet.select(fn.strftime('%W', Tweet.date).alias('week'), fn.Count(Tweet.id.distinct())).where(
            Tweet.user == acc).group_by(fn.strftime('%W', Tweet.date)).tuples():
        week = int(week)
        for i in range(1, week - prev_week):
            data.append(0)
        data.append(count)
        prev_week = week

    #2018 ima 53 tednov
    for i in range(0, 53 - len(data)):
        data.append(0)

    # normalizacija v interval [0 - 1.0]
    #norm = Normalize()
    #data = norm(data)

    ax1.plot(data, 'b-', label=val)

    for week, label in important.items():
        ax1.axvline(x=week)
        ax1.text(week+0.1, 1, label, rotation=90, verticalalignment='bottom')

    ax1.legend(loc='upper left')

plt.savefig('graf.png',bbox_inches='tight')