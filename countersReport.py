import datetime
import json
import os.path

today = datetime.datetime.today().strftime('%Y-%m-%d')
dailyZeroArray = {
    "www.deccanchronicle.com": 0,
    "www.dailyo.in": 0
}
weeklyZeroArray = {
    "www.deccanchronicle.com": 0,
    "www.dailyo.in": 0
}
monthlyZeroArray = {
    "www.deccanchronicle.com": 0,
    "www.dailyo.in": 0
}


def addCounter(domain):
    jsondata = os.path.exists("./counters/%s_daily-counters.json" %today)
    if jsondata:
        with open('./counters/%s_daily-counters.json' % today) as fp:
            dailyCounterArray = json.load(fp)
        dailyCounterArray[domain] += 1
        with open('./counters/%s_daily-counters.json' % today, 'w') as fp:
            json.dump(dailyCounterArray, fp)
    else:
        with open('./counters/%s_daily-counters.json' % today, 'w') as fp:
            json.dump(dailyZeroArray, fp)

        with open('./counters/%s_daily-counters.json' % today) as fp:
            dailyCounterArray = json.load(fp)
        dailyCounterArray[domain] += 1
        with open('./counters/%s_daily-counters.json' % today, 'w') as fp:
            json.dump(dailyCounterArray, fp)
