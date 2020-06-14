import random
import urllib.request as r
import datetime as d
from typing import List

import icalendar as i


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

    return Event(vevent.get('summary'), start, end)


def normalize_dt(dt) -> d.datetime:
    if type(dt) is d.date:
        # turn it into a datetime with time of 0
        return d.datetime.combine(dt, d.time(tzinfo=None))

    return dt.replace(tzinfo=None)


def vevent_start(vevent):
    return normalize_dt(vevent.decoded('dtstart'))


def vevent_end(vevent: i.Event) -> d.datetime:
    try:
        return normalize_dt(vevent.decoded('dtend'))
    except KeyError:
        return vevent_start(vevent)


def todays_events(ical: i.Calendar) -> List[i.Event]:
    return [vevent_to_event(vevent) for vevent in ical.walk('vevent') if is_today(vevent)]


def is_today(vevent: i.Event) -> bool:
    return event_occurs_on_day(vevent, d.datetime.now())


def event_occurs_on_day(vevent: i.Event, day: d.datetime) -> bool:
    if 'rrule' not in vevent:
        return vevent_start(vevent) <= day < vevent_end(vevent)

    # Now we now the event is recurring

    try:
        recur_end = normalize_dt(vevent['rrule']['until'][0])
    except KeyError:
        recur_end = None

    if recur_end and recur_end < day:
        return False

    frequency = vevent['rrule']['freq'][0]

    if frequency == 'DAILY':
        return True

    if frequency == 'WEEKLY':
        return int_to_weekday_str(day.weekday()) in vevent['rrule']['byday']

    return False


def int_to_weekday_str(day: int) -> str:
    return {
        0: 'MO',
        1: 'TU',
        2: 'WE',
        3: 'TH',
        4: 'FR',
        5: 'SA',
        6: 'SU',
    }[day]


def get_ical_from_link(link: str) -> i.Calendar:
    # Download the calendar and display today's events
    res = r.urlopen(link)
    return i.Calendar.from_ical(res.read())


def get_schedule_from_link(link: str) -> VisualSchedule:
    ical = get_ical_from_link(link)
    return VisualSchedule(ical.get('X-WR-CALNAME'), todays_events(ical))
