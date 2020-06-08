from dotenv import load_dotenv
from flask import Flask, render_template, request, abort
from schedule import get_schedule_from_link, Event

load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/pie')
def pie():
    calendar_link = request.args.get('link')

    if not calendar_link:
        abort(422, 'Invalid calendar link supplied')

    schedule = get_schedule_from_link(calendar_link)

    schedule_items = list(map(event_to_stroke, schedule.events))

    return render_template('pie.html', schedule=schedule, schedule_items=schedule_items)


def event_to_stroke(event: Event):
    start, end = event.start_time.hour, event.end_time.hour

    # offset is negative, and add +25
    offset = -hour_to_percent(start) + 25

    length = hour_to_percent(end - start)

    after = 100 - length

    return event.title, offset, length, after, event.color


def hour_to_percent(val):
    return val * (100 / 24)
