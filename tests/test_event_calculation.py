import unittest
from datetime import datetime

import pytz
from icalendar import Event

import schedule as s


def single_event():
    return Event.from_ical("""
BEGIN:VEVENT
DTSTART:20200608T130000Z
DTEND:20200608T133000Z
DTSTAMP:20200609T185535Z
UID:284q4rq62551m7ndij524dt3kr@google.com
CREATED:20200603T165951Z
LAST-MODIFIED:20200607T144853Z
SUMMARY:One time event
END:VEVENT
""")


def daily_event():
    return Event.from_ical("""
BEGIN:VEVENT
DTSTART;TZID=America/Toronto:20200604T100000
DTEND;TZID=America/Toronto:20200604T130000
RRULE:FREQ=DAILY
DTSTAMP:20200605T051851Z
UID:6j3hkhv3d41mbeo83cpi784h6t@google.com
CREATED:20200605T013629Z
DESCRIPTION:
LAST-MODIFIED:20200605T013629Z
LOCATION:
SEQUENCE:0
STATUS:CONFIRMED
SUMMARY:Class
TRANSP:OPAQUE
END:VEVENT
""")


def weekly_event():
    return Event.from_ical("""
BEGIN:VEVENT
DTSTART;TZID=America/Toronto:20200604T100000
DTEND;TZID=America/Toronto:20200604T130000
RRULE:FREQ=WEEKLY;WKST=SU;BYDAY=FR,MO,TH,TU,WE,SU,SA
DTSTAMP:20200605T204051Z
UID:6j3hkhv3d41mbeo83cpi784h6t@google.com
CREATED:20200605T013629Z
DESCRIPTION:
LAST-MODIFIED:20200605T204040Z
LOCATION:
SEQUENCE:0
STATUS:CONFIRMED
SUMMARY:Class
TRANSP:OPAQUE
END:VEVENT
""")


class EventCalculation(unittest.TestCase):
    date = datetime(2020, 6, 15, tzinfo=pytz.timezone('America/Toronto'))

    def test_calculates_if_single_event_occurs_on_date(self):
        self.assertTrue(s.event_occurs_on_day(single_event(), self.date))

    def test_calculates_if_daily_event_occurs_on_date(self):
        self.assertTrue(s.event_occurs_on_day(daily_event(), self.date))

    def test_calculates_if_weekly_event_occurs_on_date(self):
        self.assertTrue(s.event_occurs_on_day(weekly_event(), self.date))


if __name__ == '__main__':
    unittest.main()
