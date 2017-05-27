import argparse
import requests
from datetime import datetime, timedelta
import json
import icalendar

TOGGL_URL_TEMPLATE = "https://www.toggl.com/api/v8/time_entries?start_date={}&end_date={}"
TOGGL_TIME_FORMAT = "%Y-%m-%dT%H:%M:00Z"

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Saves Toggl time entries to iCal file')
    parser.add_argument('-d', '--days', type=int, help='Retrieve entries for this number of days from now',
                        required=True, default=14)
    parser.add_argument('-t', '--token', help='Your API token; take it from https://toggl.com/app/profile',
                        required=True, default=None)

    args = parser.parse_args()
    api_token = args.token
    days = args.days

    end_date = datetime.now().strftime(TOGGL_TIME_FORMAT.format(TOGGL_TIME_FORMAT))
    start_date = (datetime.now() - timedelta(days=int(days))).strftime(TOGGL_TIME_FORMAT.format(TOGGL_TIME_FORMAT))

    response = requests.get(TOGGL_URL_TEMPLATE.format(start_date, end_date), auth=(api_token, 'api_token'))
    if response.status_code == 200:
        time_entries = json.loads(response.text)
        print("Got {} entries".format(len(time_entries)))
    else:
        print("Get error code from the API: {}".format(response.status_code))

