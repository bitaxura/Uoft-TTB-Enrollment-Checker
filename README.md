# TTB Scraper

Lightweight Python script that checks University of Toronto Timetable Builder (TTB) course sections for open seats and sends notifications to a Discord channel via webhook.

- Script: [main.py](main.py)
- Key settings: [`main.division`](main.py), [`main.sessions`](main.py), [`main.course_code`](main.py), [`main.sections`](main.py), [`main.send_discord_message`](main.py)

## Features
- Checks course and section availability using TTB’s public API.
- Monitors enrollment changes and compares current spots to maximum capacity.
- Sends notifications to a Discord channel when seats become available.

## Prerequisites
- Python 3.8+
- A Discord webhook URL (Server Settings → Integrations → Webhooks)

Install dependency:
```bash
pip install requests
```

## Configuration
Edit [main.py](main.py):

- [`main.division`](main.py): Campus/division code. Examples: `"ERIN"` (UTM), `"ARTSC"` (UTSG FAS).
- [`main.sessions`](main.py): Session codes as strings. Format: `"YYYY9"` (Fall), `"YYYY1"` (Winter). Example: `["20259", "20261"]`.
- [`main.course_code`](main.py): Course codes to check. Example: `["MAT223H5", "CSC207H5"]`.
- [`main.sections`](main.py): Section codes. Example: `[["PRA0101", "LEC0101"]]`.
- Set your Discord webhook URL in [`main.send_discord_message`](main.py).

Example:
```python
# Example values
division = "ARTSC"
sessions = ["20259", "20261"]
course_code = ["MAT223H5", "CSC207H5"]
sections = [["LEC0101", "PRA0101"]]

def send_discord_message(message: str):
    webhook_url = r"https://discord.com/api/webhooks/XXXXXXXX/XXXXXXXX"
    # ...
```

## Run
```bash
python main.py
```

Each run checks all configured courses/sections and posts messages like:
- “There are 3 spots available in section LEC0101 in course CSC207H5.”
- “Section PRA0101 of course MAT223H5 is full.”

## Tips
- Schedule periodic checks with Task Scheduler (Windows) or cron (Linux/macOS).
- Github actions can be used to setup automation
- TTB may change response formats; this script uses simple string parsing and may need updates.
- Ensure session, division, course, and section codes exactly match TTB.

## License
MIT — see [LICENSE](LICENSE).

## Disclaimer
For personal/educational use. Respect U of T policies and rate limits.