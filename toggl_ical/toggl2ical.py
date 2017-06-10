import argparse
import requests
from datetime import datetime, timedelta
import json
import icalendar
from dateutil.parser import parse

TOGGL_URL_TEMPLATE = "https://www.toggl.com/api/v8/time_entries?start_date={}&end_date={}"
TOGGL_TIME_FORMAT = "%Y-%m-%dT%H:%M:00Z"


def get_entries(api_token, days):
    end_date = datetime.now().strftime(TOGGL_TIME_FORMAT.format(TOGGL_TIME_FORMAT))
    start_date = (datetime.now() - timedelta(days=int(days))).strftime(TOGGL_TIME_FORMAT.format(TOGGL_TIME_FORMAT))

    response = requests.get(TOGGL_URL_TEMPLATE.format(start_date, end_date), auth=(api_token, 'api_token'))
    if response.status_code == 200:
        time_entries = json.loads(response.text)
        print("Got {} time entries".format(len(time_entries)))
        return time_entries
    else:
        print("Get error code from the API: {}".format(response.status_code))
        return []


def build_calendar(time_entries):
    # Create the Calendar
    calendar = icalendar.Calendar()
    calendar.add('prodid', "toggl2ical")
    calendar.add('version', '2.0')
    calendar.add('CALSCALE', 'GREGORIAN')
    calendar.add('X-WR-CALNAME', 'Toggl events')
    calendar.add('method', 'publish')

    for entry in time_entries:
        event = icalendar.Event()
        if all(field in entry for field in ["start", "description", "id"]):
            event.add('summary', entry["description"])
            if "tags" in entry:
                event.add('description', ", ".join(entry["tags"]))
            event.add('uid', entry["id"])
            event.add('dtstart', parse(entry["start"]))
            if "stop" in entry:
                event.add('dtend', parse(entry["stop"]))
            else:
                event.add('dtend', datetime.now())
            event.add('dtstamp', datetime.now())
            # event.add('STATUS', 'CANCELLED')
            calendar.add_component(event)

    ical = str(calendar.to_ical()).replace("\\r\\n", "\n").strip("b'").strip("'")
    return ical

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Saves Toggl time entries to iCal file')
    parser.add_argument('-d', '--days', type=int, help='Retrieve entries for this number of days from now',
                        required=True, default=14)
    parser.add_argument('-t', '--token', help='Your API token; take it from https://toggl.com/app/profile',
                        required=True, default=None)

    args = parser.parse_args()

    entries = get_entries(args.token, args.days)
    ical_text = build_calendar(entries)
    with open("calendar.ics", "w") as file:
        file.write(ical_text)



