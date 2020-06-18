import random
import urllib.request as r
import datetime as d
from typing import List

import ics as i


class Event:
    colors = ['red', 'blue', 'green', 'yellow']

    def __init__(self, title: str, start_time, end_time, color: str = None):
        self.title = title
        self.color = color or self.new_color()
        self.start_time = start_time.hour if type(start_time) is 'datetime' else start_time
        self.end_time = end_time.hour if type(end_time) is 'datetime' else end_time

    def range(self) -> str:
        return '{:%I:%M%p} - {:%I:%M%p}'.format(self.start_time, self.end_time)

    def new_color(self):
        return random.choice(self.colors)


class VisualSchedule:
    def __init__(self, title: str, events: List[Event]):
        self.title = title
        self.events = events


def vevent_to_event(vevent: i.Event):
    start = vevent_start(vevent)
    end = vevent_end(vevent)

    return Event(vevent.name, start, end)


def normalize_dt(dt) -> d.datetime:
    if type(dt) is d.date:
        # turn it into a datetime with time of 0
        return d.datetime.combine(dt, d.time(tzinfo=None))

    return dt.replace(tzinfo=None)


def vevent_start(vevent):
    return normalize_dt(vevent.begin)


def vevent_end(vevent: i.Event) -> d.datetime:
    try:
        return normalize_dt(vevent.end)
    except KeyError:
        return vevent_start(vevent)


def todays_events(ical: i.Calendar) -> List[Event]:
    return [vevent_to_event(vevent) for vevent in ical.timeline.today()]


def ical_name(ical: i.Calendar) -> str:
    return next((x.value for x in ical.extra if x.name == 'X-WR-CALNAME'), '')


def fetch_link(link: str) -> str:
    res = r.urlopen(link)
    body = res.read()
    if type(body) is bytes:
        body = body.decode()
    return body


def get_schedule_from_link(link: str) -> VisualSchedule:
    ical = i.Calendar(fetch_link(link))
    return VisualSchedule(ical_name(ical), todays_events(ical))
