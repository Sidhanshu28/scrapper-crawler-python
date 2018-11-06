import json
import csv
import os.path
import datetime

def csvExporter():
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    with open('./counters/%s_daily-counters.json' % today) as fp:
        dailyCounterArray = json.load(fp)

    tempArr = []
    for k in dailyCounterArray:
        tempArr.append((k,dailyCounterArray[k]))
    tempArr.insert(0, ("Websites Links", "Counters"))
    dailyCounterArray = dict(tempArr)
    with open('./counters/%s_daily-counters.csv' % today, 'w') as csv_file:
        writer = csv.writer(csv_file)
        for key, value in dailyCounterArray.items():
            writer.writerow([key, value])