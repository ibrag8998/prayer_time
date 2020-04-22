#!/usr/bin/env python
from datetime import datetime
import subprocess

import requests


def notify(title, desc):
    subprocess.call(['notify-send', '--hint=int:transient:1', \
            title, desc])


def get_pending(timings):
    for p, t in timings.items():
        prayer = (p, t)
        clean_t = f'{dt.year}-{dt.month:02}-{dt.day:02} {t[:5]}:00'
        prayer_dt = datetime.strptime(clean_t, '%Y-%m-%d %H:%M:%S')
        if prayer_dt >= dt:
            return prayer
    return ('Fajr', timings['Fajr'])


def select_by_date(data):
    for e in data:
        if int(e['date']['gregorian']['day']) == dt.day:
            return e['timings']
    notify('select_by_date', 'Something went wrong...')
    exit()


dt = datetime.now()
url = 'http://api.aladhan.com/v1/calendar'
payload = {
    'latitude': 42.958944,
    'longitude': 47.499378,
    'month': dt.month,
    'year': dt.year,
    'method': 3
}

r = requests.get(url, params=payload)
if r.ok:
    data = r.json()['data']
else:
    notify('requests.get', 'Something went wrong...')
    exit()

notify(*get_pending(select_by_date(data)))

