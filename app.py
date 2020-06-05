from flask import Flask
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    calendars = [
        'ical-url.com'
    ]

    return '''My calendars:
{}
'''.format(calendars)
