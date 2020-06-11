import random
import urllib.request as r
import datetime as d
from typing import Optional

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
    title = ''
    events: [Event] = []

    def __init__(self, title: str, tz: d.tzinfo, events: [Event]):
        self.title = title
        self.tz = tz or pytz.UTC
        self.events = events


def new_event(event: i.Event):
    return Event(
        event.get('summary'),
        event.decoded('dtstart'),
        event.decoded('dtend')
    )


def get_cal_tz(cal: i.Calendar) -> Optional[d.tzinfo]:
    try:
        return cal.walk('vtimezone')[0].to_tz()
    except KeyError:
        return None


def todays_events(cal: i.Calendar) -> [i.Event]:
    return [new_event(event) for event in cal.walk('vevent') if is_today(event, get_cal_tz(cal))]


def is_today(event: i.Event, tz=pytz.UTC) -> bool:
    return event_occurs_on_day(event, d.datetime.now(tz=tz))


def event_occurs_on_day(event: i.Event, day: d.datetime) -> bool:
    if 'rrule' not in event:
        return event.decoded('dtstart') < day

    # Now we now the event is recurring

    # if end and end is before today (for VEVENTS check UNTIL or COUNT)
    #     return False

    frequency = event['rrule']['freq'][0]

    if frequency == 'DAILY':
        return True

    if frequency == 'WEEKLY':
        return int_to_weekday_str(day.weekday()) in event['rrule']['byday']

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


def get_cal_from_link(link: str) -> i.Calendar:
    # Download the calendar and display today's events
    res = r.urlopen(link)
    return i.Calendar.from_ical(res.read())


def get_schedule_from_link(link: str) -> VisualSchedule:
    cal = get_cal_from_link(link)
    return VisualSchedule(cal.get('X-WR-CALNAME'), get_cal_tz(cal), todays_events(cal))
