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
    return True


def event_occurs_on_day(event: i.Event, day) -> bool:
    # if recurring
    # AND recurs on this day of the week etc.
    # AND start is before today and end is after today (if they exist)

    # OR date is today
    pass


def get_cal_from_link(link: str) -> i.Calendar:
    # Download the calendar and display today's events
    res = r.urlopen(link)
    return i.Calendar.from_ical(res.read())


def get_schedule_from_link(link: str) -> VisualSchedule:
    cal = get_cal_from_link(link)
    return VisualSchedule(cal.get('X-WR-CALNAME'), todays_events(cal))
