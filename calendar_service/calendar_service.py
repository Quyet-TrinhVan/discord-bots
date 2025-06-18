from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import pytz

SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = 'credentials/discord_bots.json'
CALENDAR_ID = 'quyettv1302@gmail.com'
TIMEZONE = 'Asia/Ho_Chi_Minh'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('calendar', 'v3', credentials=credentials)
tz = pytz.timezone(TIMEZONE)

def add_event(summary, date_str, time_str):
    start_time = tz.localize(datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M"))
    end_time = start_time + timedelta(hours=1)

    event = {
        'summary': summary,
        'start': {'dateTime': start_time.isoformat(), 'timeZone': TIMEZONE},
        'end': {'dateTime': end_time.isoformat(), 'timeZone': TIMEZONE}
    }
    service.events().insert(calendarId=CALENDAR_ID, body=event).execute()


def delete_event(date_str, time_str=None, title=None):
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


def update_event(date_str, old_time_str, old_title, new_summary=None, new_date_str=None, new_time_str=None):
    events = get_events_for_date(date_str)
    updated = False

    for e in events:
        event_title = e.get("summary", "").lower()
        event_time_str_full = e.get("start", {}).get("dateTime", None)

        if event_time_str_full:
            event_time = event_time_str_full[11:16]

            if old_title.lower() in event_title and old_time_str == event_time:
                event_id = e['id']
                current_event = service.events().get(calendarId=CALENDAR_ID, eventId=event_id).execute()

                if new_summary:
                    current_event['summary'] = new_summary

                if new_date_str or new_time_str:
                    old_start_datetime = datetime.fromisoformat(current_event['start']['dateTime'])
                    target_date = datetime.strptime(new_date_str, "%Y-%m-%d").date() if new_date_str else old_start_datetime.date()
                    target_time = datetime.strptime(new_time_str, '%H:%M').time() if new_time_str else old_start_datetime.time()
                    new_start_datetime_local = tz.localize(datetime.combine(target_date, target_time))
                    new_end_datetime_local = new_start_datetime_local + (datetime.fromisoformat(current_event['end']['dateTime']) - old_start_datetime)

                    current_event['start']['dateTime'] = new_start_datetime_local.isoformat()
                    current_event['end']['dateTime'] = new_end_datetime_local.isoformat()

                service.events().update(calendarId=CALENDAR_ID, eventId=event_id, body=current_event).execute()
                print(f"✅ Updated event: '{old_title}' on {date_str} at {old_time_str}")
                updated = True
                break

    if not updated:
        print(f"❌ No event found to update with title '{old_title}' on {date_str} at {old_time_str}!")
    return updated


def get_events_for_date(date_str):
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
