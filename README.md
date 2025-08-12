

# TTB Enrollment Checker

This project provides two ways to get notified about open seats in University of Toronto Timetable Builder (TTB) course sections:

1. **Discord Bot** (recommended): Interact with a Discord bot to add, remove, and list courses, and receive notifications in a channel.
2. **Webhook Script**: A standalone script that posts directly to a Discord webhook when spots are available.

---

## Option 1: Discord Bot

- Main bot: [`bot.py`](bot.py)
- API logic: [`api_bot.py`](api_bot.py)

### Features
- Checks course and section availability using TTB’s public API.
- Compares current enrollment vs. max capacity and notifies when seats are available.
- Posts to a Discord channel and mentions the user who added the course.
- Add, delete, and list your watched courses via Discord commands.

### Prerequisites
- Python 3.8+
- A Discord bot token ([guide](https://discordpy.readthedocs.io/en/stable/discord.html))
- Your Discord channel ID (right-click channel → Copy ID)

Install dependencies:
```bash
pip install discord.py python-dotenv aiohttp
```

### Configuration

1. Copy `.env.example` to `.env` and fill in your bot token and channel ID:
    ```env
    DISCORD_TOKEN=your_discord_bot_token_here
    CHANNEL_ID=your_channel_id_here
    ```

2. Start the bot:
    ```bash
    python bot.py
    ```

3. Use Discord commands in your server:
    - `!add {dict}` — Add a course to watch. Example:
      ```
      !add {'division': 'ERIN', 'sessions': '20259', 'course_code': 'CSC207H5', 'sections': ['PRA0119', 'PRA0101']}
      ```
      (Your Discord user ID is automatically attached.)
    - `!myentries` — List your watched courses.
    - `!delete N` — Delete your Nth entry (see `!myentries`).
    - `!run_api` — Manually trigger a check for open spots.

**Field notes**:
- Division: "ERIN" (UTM), "ARTSC" (UTSG FAS), "SCAR" (UTSC), "APSC" (Engineering).
- Sessions:
    - "YYYY9" (Fall)
    - "YYYY1" (Winter)
    - "YYYY5" (Summer June-August)
    - "YYYY5F" (Summer May-June)
    - "YYYY5S" (Summer July-August)
- Course_code: Must include the campus suffix (e.g., H1/H3/H5).
- Sections: List of section codes exactly as shown in TTB/Acorn (e.g., LEC0101, PRA0101, TUT0103).

### How it works

- The bot stores all added courses in memory (not persistent).
- Every 6 hours, it checks all watched courses and posts to the configured channel if spots are available, mentioning the user who added the course.
- You can also trigger a check manually with `!run_api`.

Example notification:
> There are 3 spots available in section LEC0101 in course CSC207H5. <@your_user_id>

### Tips
- Ensure session, division, course, and section codes exactly match TTB/acorn.
- Enable Discord Developer Mode to copy user and channel IDs.
- The bot must have permission to read/send messages in your target channel.

### Known Issues
- TTB may change response formats; this script uses simple string parsing and may need updates.
- All course data is lost when the bot restarts (no database/persistence).


---

## Option 2: Webhook Script (Legacy)

If you prefer a simple script that posts directly to a Discord webhook, use [`api_standalone.py`](api_standalone.py). This does not require a bot user or channel ID, just a Discord webhook URL.

### Features
- Checks course and section availability using TTB’s public API.
- Posts to a Discord webhook and mentions a specific user by ID.
- Simple to set up for single-user or single-channel notifications.

### Prerequisites
- Python 3.8+
- A Discord webhook URL (Server Settings → Integrations → Webhooks)

Install dependency:
```bash
pip install requests
```

### Configuration
1. Edit [`api_standalone.py`](api_standalone.py):
        - Set your Discord webhook URL in `send_discord_message`:
            ```python
            webhook_url = r"YOUR_DISCORD_WEBHOOK_URL_HERE"  # paste your webhook URL
            ```
        - Define the list of courses to watch in `courses`:
            ```python
            courses = [
                    {
                            "division": "ERIN",
                            "sessions": "20259",
                            "course_code": "CSC207H5",
                            "sections": ["PRA0119", "PRA0101"],
                            "user_id": "700329119761448910"
                    },
                    # Add more dicts for additional courses
            ]
            ```

**Field notes**:
- division: "ERIN" (UTM), "ARTSC" (UTSG FAS), "SCAR" (UTSC), "APSC" (Engineering).
- sessions:
    - "YYYY9" (Fall)
    - "YYYY1" (Winter)
    - "YYYY5" (Summer June-August)
    - "YYYY5F" (Summer May-June)
    - "YYYY5S" (Summer July-August)
- course_code: Must include the campus suffix (e.g., H1/H3/H5).
- sections: List of section codes exactly as shown in TTB/Acorn (e.g., LEC0101, PRA0101, TUT0103).
- user_id: Enable Discord Developer Mode → right-click user → Copy ID.
### Run
```bash
python api_standalone.py
```

Each run checks all configured courses/sections and posts messages like:
> There are 3 spots available in section LEC0101 in course CSC207H5. <@your_user_id>

---

## License
MIT - see [LICENSE](LICENSE).

## Disclaimer
For personal/educational use. Respect U of T policies and rate limits.