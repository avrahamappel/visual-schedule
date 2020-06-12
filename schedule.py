import random
import urllib.request as r
import datetime as d
from typing import Optional, List

import pytz
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
        random.seed(30)
        return random.choice(self.colors)


class VisualSchedule:
    def __init__(self, title: str, tz: d.tzinfo, events: List[Event]):
        self.title = title
        self.tz = tz or pytz.UTC
        self.events = events


def vevent_to_event(vevent: i.Event):
    return Event(
        vevent.get('summary'),
        normalize_dt(vevent.decoded('dtstart')),
        normalize_dt(vevent.decoded('dtend'))
    )


def normalize_dt(dt) -> d.datetime:
    """Make sure the date is a tz-aware instance of datetime.datetime"""

    # TODO make sure it's tz-aware

    if type(dt) is d.date:
        # turn it into a datetime with time of 0
        return d.datetime.combine(dt, d.time())

    return dt


def get_cal_tz(ical: i.Calendar) -> Optional[d.tzinfo]:
    try:
        return ical.walk('vtimezone')[0].to_tz()
    except KeyError:
        return None


def todays_events(ical: i.Calendar) -> List[i.Event]:
    return [vevent_to_event(vevent) for vevent in ical.walk('vevent') if is_today(vevent, get_cal_tz(ical))]


def is_today(vevent: i.Event, tz=pytz.UTC) -> bool:
    return event_occurs_on_day(vevent, d.datetime.now(tz=tz))


def event_occurs_on_day(vevent: i.Event, day: d.datetime) -> bool:
    if 'rrule' not in vevent:
        return normalize_dt(vevent.decoded('dtstart')) < day

    # Now we now the event is recurring

    # if end and end is before today (for VEVENTS check UNTIL or COUNT)
    #     return False

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
    return VisualSchedule(ical.get('X-WR-CALNAME'), get_cal_tz(ical), todays_events(ical))
