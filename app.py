from dotenv import load_dotenv
from flask import Flask, render_template
import icalendar as i
import urllib.request as r

load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    calendar_links = [
        'https://calendar.google.com/calendar/ical/hbo7a25pd64ebpln1ge3trsopk%40group.calendar.google.com/private-9403c3cc5d11928f79f0652dea277ff9/basic.ics'
    ]

    calendars = (get_cal_from_link(link) for link in calendar_links)
    summaries = [(cal.get('X-WR-CALNAME'), todays_events(cal)) for cal in calendars]

    return render_template('home.html', calendars=summaries)


def get_cal_from_link(link: str) -> i.Calendar:
    # Download the calendar and display today's events
    res = r.urlopen(link)
    return i.Calendar.from_ical(res.read())


def todays_events(cal: i.Calendar) -> [i.Event]:
    return [event for event in cal.walk('vevent') if is_today(event)]


def is_today(event: i.Event) -> bool:
    return True


def event_occurs_on_day(event: i.Event, day) -> bool:
    # if recurring
    # AND recurs on this day of the week etc.
    # AND start is before today and end is after today (if they exist)

    # OR date is today
    pass
