import discord
import os
from dotenv import load_dotenv
from gemini_utils import extract_calendar_command
from calendar_service import add_event, get_events_for_date, delete_event, update_event
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Bot is ready: {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    prompt = message.content
    parsed = extract_calendar_command(prompt)
    
    if not parsed:
        await message.channel.send("❌ Can't understand the content, please try again.")
        return

    intent = parsed['intent']
    date = parsed.get('date')
    time = parsed.get('time')
    title = parsed.get('title') or "schedule"
    
    new_summary = parsed.get('new_summary')
    new_date = parsed.get('new_date')
    new_time = parsed.get('new_time')

    if intent == "add_event":
        if not date:
            await message.channel.send("❌ Missing date.")
            return

        title_lower = title.lower()

        if "working" in title_lower or "làm việc" in title_lower:
            success = add_event(title, date_str=date)
            if success:
                await message.channel.send(f"✅ Added work schedule on {date} from 08:00 to 17:30")
            else:
                await message.channel.send("❌ Event already exists!")
        else:
            if not time:
                await message.channel.send("❌ Missing time for this event.")
                return

            default_duration = 60
            success = add_event(
                summary=title,
                date_str=date,
                time_str=time,
                duration_minutes=default_duration
            )
            if success:
                await message.channel.send(
                    f"📌 Added event '{title}' on {date} at {time} for {default_duration} minutes."
                )
            else:
                await message.channel.send("❌ Event already exists!")

    elif intent == "check_schedule":
        events = get_events_for_date(date)
        if not events:
            await message.channel.send("🎉 You are free that day!")
        else:
            reply = f"📅 Schedule for {date}:\n"
            for e in events:
                time = e['start'].get('dateTime', 'N/A')[11:16]
                reply += f"- {time} | {e.get('summary', 'No title')}\n"
            await message.channel.send(reply)
    elif intent == "delete_event":
        if delete_event(date, time, title):
            await message.channel.send(f"🗑️ Deleted event '{title}' on {date} at {time or 'any time'}")
        else:
            await message.channel.send("❌ No event to delete!")
    elif intent == "update_event":
        if not (date and time and title):
            await message.channel.send("❌ To update an event, please provide the **original date, time, and title** of the event you want to change.")
            return
        
        if update_event(date, time, title, new_summary, new_date, new_time):
            update_details = []
            if new_summary:
                update_details.append(f"new title: '{new_summary}'")
            if new_date:
                update_details.append(f"new date: {new_date}")
            if new_time:
                update_details.append(f"new time: {new_time}")

            if update_details:
                await message.channel.send(f"✏️ Updated event '{title}' on {date} at {time}. Now has {' and '.join(update_details)}.")
            else:
                await message.channel.send(f"✏️ Event '{title}' on {date} at {time} found, but no new details were provided for update.")
        else:
            await message.channel.send(f"❌ Could not find event '{title}' on {date} at {time} to update.") 
client.run(TOKEN)
