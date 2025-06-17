# Discord Calendar Bot

A Discord bot that uses Google Calendar and Gemini AI to help you manage schedules and events directly from your Discord server.

## Features

- Add work schedules and custom events via prompts.
- Check your schedule for a specific date.
- Uses Google Calendar API for event management.
- Natural language command parsing powered by Gemini AI.

## Setup

### 1. Clone the repository

```sh
git clone https://github.com/yourusername/discord-bots.git
cd discord-bots
```

### 2. Set up the Python environment

```sh
python -m venv discord_env
discord_env\\Scripts\\activate
pip install -r requirements.txt
```

### 3. Environment Variables

Create a `.env` file in `calendar_service/` with:

```
DISCORD_TOKEN=your_discord_token
GEMINI_API_KEY=your_gemini_api_key
```

### 4. Google Calendar Credentials

- Place your Google service account JSON in `calendar_service/credentials/discord_bots.json`.
- Share your Google Calendar with the service account email.

### 5. Run the Bot

```sh
cd calendar_service
python bot.py
```

## Usage

- Add a work schedule:  
  `Add a work schedule on 2025-06-18 at 09:00`
- Add a custom event:  
  `Create an event called Meeting on 2025-06-19 at 15:30`
- Check your schedule:  
  `What is my schedule for 2025-06-20?`

## License

MIT License. See [LICENSE](LICENSE).
