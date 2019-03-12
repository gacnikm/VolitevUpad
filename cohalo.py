import json
import os
import urllib.request
import datetime
from parsel import Selector

from db import db, Tweet
from racuni import accounts


PATH = os.path.dirname(os.path.abspath(__file__))
db.init(os.path.join(PATH, 'db.sqlite'))
db.connect()
db.create_tables([Tweet])

headers = {
    "accept": "application/json,*/*;q=0.8",
    "accept-language": "en,sl;q=0.9,en-US;q=0.8",
    "cache-control": "no-cache",
    "dnt": "1",
    'X-Requested-With': "XMLHttpRequest",
    "pragma": "no-cache",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "host" :"twitter.com"
}

REQ = "https://twitter.com/i/search/timeline"
REQ = "https://twitter.com/search?vertical=default&f=tweets&q=from:JJansaSDS since:{} until:{}&src=typd&qf=off"
nums = []
values = {
    "f": "tweets",
    "vertical": "default",
    "src": "typd",
    "qf": "off"
}

for i in range(3):
    print("ROUND:", i)

    start = datetime.date(2018, 1, 1)
    end = datetime.date(2019, 1, 1)
    step = datetime.timedelta(days=1)

    while start < end:
        next_date = start + step

        for acc, name in accounts.items():
            #print("ACC:", acc)

            values['q'] = "from:{} since:{} until:{}".format(acc, start.strftime('%Y-%m-%d'),
                                                             next_date.strftime('%Y-%m-%d'))
            url = REQ + "?" + urllib.parse.urlencode(values)

            req = urllib.request.Request(url, headers=headers)
            response = urllib.request.urlopen(req)
            page = response.read()

            try:
                json_data = json.loads(page.decode('utf-8'))
                sel = Selector(json_data['items_html'])
                tweets = sel.xpath("//div[contains(@class,'tweet')]/@data-tweet-id").extract()
                for tweet in tweets:
                    t, created = Tweet.get_or_create(id=tweet, user=acc, date=start)
                    if created:
                        print("NEW TWEET:", tweet)

                if json_data['has_more_items']:
                    print("HAS MORE:", start)
            except:
                print("ERROR:", start)

        start = next_date
    print("ROUND END:", i)
