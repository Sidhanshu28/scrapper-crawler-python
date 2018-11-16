import datetime
import json
import os.path
from csvExportFile import csvExporter

today = datetime.datetime.today().strftime('%Y-%m-%d')
dailyZeroArray = {
    "www.deccanchronicle.com": 0,
    "www.dailyo.in": 0,
    "www.dnaindia.com/analysis":0,
    "www.firstpost.com/category/politics":0,
    "www.forbesindia.com":0,
    "www.frontline.in":0,
    "www.hindustantimes.com":0,
    "indiatoday.intoday.in/calendar":0,
    "www.livemint.com/opinion":0,
    "www.ndtv.com":0,
    "www.news18.com":0,
    "www.outlookindia.com":0,
    "www.outlookindia.com":0,
    # "www.rediff.com/news/interviews10.html":0,
    # "www.rediff.com/news/columns10.html":0,
    "scroll.in":0,
    "blogs.economictimes.indiatimes.com":0,
    "www.financialexpress.com":0,
    "www.thehindu.com":0,
    "www.thehindubusinessline.com":0,
    "www.huffingtonpost.in/the-blog":0,
    "theindianeconomist.com":0,
    "indianexpress.com/opinion":0,
    "www.newindianexpress.com/Opinions":0,
    "www.dailypioneer.com/columnists":0,
    "blogs.timesofindia.indiatimes.com":0,
    "www.tribuneindia.com/news/opinion":0,
    "thewire.in":0,
    "www.telegraphindia.com/opinion":0,

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
        csvExporter()
    else:
        with open('./counters/%s_daily-counters.json' % today, 'w') as fp:
            json.dump(dailyZeroArray, fp)

        with open('./counters/%s_daily-counters.json' % today) as fp:
            dailyCounterArray = json.load(fp)
        dailyCounterArray[domain] += 1
        with open('./counters/%s_daily-counters.json' % today, 'w') as fp:
            json.dump(dailyCounterArray, fp)
        csvExporter()
