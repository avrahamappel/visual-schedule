import icalendar as i
import urllib.request as r
from datetime import datetime


class Event:
    name = ''
    start_time = None
    end_time = None

    def __init__(self, name: str, start_time, end_time):
        self.name = name
        self.start_time: datetime = start_time
        self.end_time: datetime = end_time

    def range(self) -> str:
        return '{:%I:%M%p} - {:%I:%M%p}'.format(self.start_time, self.end_time)


class VisualSchedule:
    name = ''
    events: [Event] = []

    def __init__(self, name: str, events: [Event]):
        self.name = name
        self.events = events


def new_event(event: i.Event):
    return Event(
        event.get('summary'),
        event.decoded('dtstart'),
        event.decoded('dtend')
    )


def todays_events(cal: i.Calendar) -> [i.Event]:
    return [new_event(event) for event in cal.walk('vevent') if is_today(event)]


def is_today(event: i.Event) -> bool:
    return event_occurs_on_day(event, datetime.now())


def event_occurs_on_day(event: i.Event, day: datetime) -> bool:
    if not event['rrule']:
        return event.decoded('dtstart') > day

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
    return VisualSchedule(cal.get('X-WR-CALNAME'), todays_events(cal))
