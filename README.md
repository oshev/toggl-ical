# toggl-ical
Tool to save Toggl time entries to iCal 

DONE: 
- Receiving Toggl items in JSON.
- Creating iCal from Toggl JSON.
- Saving iCal in a file which can be imported via Google Calendar UI.

TODO: 
- Let Google Calendar get this calendar automatically. 2 options:
    - Save iCal file in a cloud with http serving.
    - Create a HTTP service which re-creates the calendar each time Google calls the service. 
