from flask import Flask, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    calendars = [
        'ical-url.com'
    ]

    return render_template('home.html', calendars=calendars)
