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
