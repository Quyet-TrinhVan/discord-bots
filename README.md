# Discord Bots Project

This repository contains Discord bots and related services, including a calendar assistant bot that integrates with Google Calendar and Gemini AI.

## Project Structure

- `calendar_service/` — Main source code for the calendar Discord bot
    - `bot.py` — Discord bot entry point
    - `calendar_service.py` — Google Calendar integration
    - `gemini_utils.py` — Natural language command parsing using Gemini AI
    - `credentials/` — Google service account credentials (not tracked in git)
    - `.env` — Environment variables for API keys and tokens
    - `README.md` — Calendar bot documentation
    - `requirements.txt` — Python dependencies
- `discord_env/` — Python virtual environment (not tracked in git)

## Main Features

- Add and check calendar events using natural language in Discord
- Google Calendar API integration for event management
- Gemini AI for parsing user prompts

## Quick Start

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/discord-bots.git
    cd discord-bots
    ```
2. Set up the Python environment:
    ```sh
    python -m venv discord_env
    discord_env\\Scripts\\activate
    pip install -r calendar_service/requirements.txt
    ```
3. Configure environment variables:
    - Create a `.env` file in `calendar_service/` with your Discord and Gemini API keys.
4. Add Google service account credentials to `calendar_service/credentials/` and share your calendar with the service account email.
5. Run the bot:
    ```sh
    cd calendar_service
    python bot.py
    ```

For more details, see `calendar_service/README.md`.

## License

MIT License. See [LICENSE](LICENSE).
