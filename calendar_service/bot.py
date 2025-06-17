import discord
import os
from dotenv import load_dotenv
from gemini_utils import extract_calendar_command
from calendar_service import add_event, get_events_for_date, delete_event
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

    if intent == "add_schedule":
        add_event("Working", date, time)
        await message.channel.send(f"✅ Added work schedule {date}")

    elif intent == "add_event":
        if date and time:
            add_event(title, date, time)
            await message.channel.send(f"📌 Added event '{title}' to {date} at {time}")
        else:
            await message.channel.send("❌ Missing date or time.")

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
client.run(TOKEN)
