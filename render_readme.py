#!/usr/bin/env python3
"""Render README.md from Jinja2 template."""
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path

try:
    from dateutil.easter import easter
    from jinja2 import Template
except ImportError as e:
    print(f"Error: Required package not installed: {e}", file=sys.stderr)
    print("Install with: uv pip install jinja2 python-dateutil", file=sys.stderr)
    sys.exit(1)


def get_greeting():
    """Get time-based greeting."""
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "Good morning"
    elif 12 <= hour < 17:
        return "Good afternoon"
    else:
        return "Good evening"


def get_seasonal_emoji(now):
    """Get seasonal emoji based on the date."""
    month = now.month
    day = now.day
    year = now.year
    date = now.date()
    day_of_year = now.timetuple().tm_yday

    # December - Christmas emojis
    christmas_emojis = ["🎄", "🎅", "❄️", "☃️", "🎁", "🔔", "🦌", "🌟", "✨", "🎄"]
    if month == 12:
        random.seed(day_of_year)
        return random.choice(christmas_emojis)

    # 2 weeks before Halloween (October 31) = around October 17
    halloween_emojis = ["🎃", "👻", "🦇", "🕷️", "🕸️", "💀", "🧙", "🧛", "🧟", "🎃"]
    if month == 10 and 15 <= day <= 31:
        random.seed(day_of_year)
        return random.choice(halloween_emojis)

    # 2 weeks before Easter
    easter_date = easter(year)
    two_weeks_before_easter = easter_date - timedelta(days=14)
    # Check if we're within a few days of 2 weeks before Easter
    if abs((date - two_weeks_before_easter).days) <= 3:
        return "🐰"

    return None


def get_day_emoji(weekday, now):
    """Get emoji based on weekday and season."""
    # Check for seasonal emojis first
    seasonal = get_seasonal_emoji(now)
    if seasonal:
        return seasonal

    # Weekdays get coffee
    if weekday in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
        return "☕"

    # Weekends get random outdoor emojis
    outdoor_emojis = ["🌴", "☀️", "🏔️", "🌊", "🌲", "⛰️", "🌅", "🌄", "🏕️", "🚵"]
    # Use day of year as seed for consistent daily randomness
    day_of_year = now.timetuple().tm_yday
    random.seed(day_of_year)
    return random.choice(outdoor_emojis)


def main():
    """Render README.md from template."""
    script_dir = Path(__file__).parent
    template_path = script_dir / "README.md.j2"
    output_path = script_dir / "README.md"

    if not template_path.exists():
        print(f"Error: Template not found at {template_path}", file=sys.stderr)
        sys.exit(1)

    # Read template
    template_content = template_path.read_text()

    # Get dynamic values
    now = datetime.now()
    weekday = now.strftime("%A")
    greeting = get_greeting()
    emoji = get_day_emoji(weekday, now)

    # Render template
    template = Template(template_content)
    rendered = template.render(
        weekday=weekday,
        greeting=greeting,
        emoji=emoji,
    )

    # Write output
    output_path.write_text(rendered)
    print(f"Rendered README.md with weekday: {weekday}, emoji: {emoji}")


if __name__ == "__main__":
    main()
