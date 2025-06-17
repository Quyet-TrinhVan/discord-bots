from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials/discord_bots.json'
CALENDAR_ID = 'quyettv1302@gmail.com'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('calendar', 'v3', credentials=credentials)
TIMEZONE = 'Asia/Ho_Chi_Minh'
tz = pytz.timezone(TIMEZONE)

def add_event(summary, date_str, time_str):
    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    start_time = tz.localize(datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M"))
    end_time = start_time + timedelta(hours=1)

    event = {
        'summary': summary,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': TIMEZONE},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': TIMEZONE}
    }
    service.events().insert(calendarId=CALENDAR_ID, body=event).execute()

def delete_event(date_str, time_str=None, title=None):
    tz = pytz.timezone("Asia/Ho_Chi_Minh")
    date = datetime.strptime(date_str, "%Y-%m-%d")
    start_of_day = tz.localize(datetime.combine(date, datetime.min.time()))
    end_of_day = tz.localize(datetime.combine(date, datetime.max.time()))

    # Lấy toàn bộ sự kiện trong ngày
    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_of_day.isoformat(),
        timeMax=end_of_day.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    deleted = False

    for e in events:
        event_title = e.get('summary', '').lower()
        event_time_str = e.get('start', {}).get('dateTime', None)
        
        match_title = True if not title else (title.lower() in event_title)
        match_time = True

        if time_str and event_time_str:
            event_time = event_time_str[11:16]
            match_time = (time_str == event_time)

        if match_title and match_time:
            service.events().delete(calendarId=CALENDAR_ID, eventId=e['id']).execute()
            print(f"✅ Deleted: {event_title} on {date_str} at {time_str or 'any time'}")
            deleted = True

    if not deleted:
        print("❌ No event to delete!")
    return deleted

def get_events_for_date(date_str):
    tz = pytz.timezone(TIMEZONE)
    date = datetime.strptime(date_str, "%Y-%m-%d")
    start_of_day = tz.localize(datetime.combine(date, datetime.min.time()))
    end_of_day = tz.localize(datetime.combine(date, datetime.max.time()))

    events_result = service.events().list(
        calendarId=CALENDAR_ID,
        timeMin=start_of_day.isoformat(),
        timeMax=end_of_day.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    return events_result.get('items', [])
