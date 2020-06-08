from dotenv import load_dotenv
from flask import Flask, render_template
from schedule import get_schedule_from_link

load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    calendar_link = 'https://calendar.google.com/calendar/ical/hbo7a25pd64ebpln1ge3trsopk%40group.calendar.google.com/private-9403c3cc5d11928f79f0652dea277ff9/basic.ics'

    schedule = get_schedule_from_link(calendar_link)

    return render_template('home.html', schedule=schedule)


@app.route('/pie')
def pie():
    schedule_items = [
        # (title, start_time, end_time, color)
        ('Shiur', 10, 11, 'blue'),
        ('English', 12, 13, 'red'),
        ('Sleep', 20, 32, 'cyan'),
    ]

    mapped = map(schedule_to_stroke, schedule_items)

    return render_template('pie.html', schedule_items=mapped)


def schedule_to_stroke(schedule):
    title, start, end, color = schedule

    # offset is negative, and add +25
    offset = -hour_to_percent(start) + 25

    length = hour_to_percent(end - start)

    after = 100 - length

    return title, offset, length, after, color


def hour_to_percent(val):
    return val * (100 / 24)
