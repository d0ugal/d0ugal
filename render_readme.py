#!/usr/bin/env python3
"""Render README.md from Jinja2 template."""
import sys
from datetime import datetime
from pathlib import Path

try:
    from jinja2 import Template
except ImportError:
    print("Error: jinja2 not installed. Install with: uv pip install jinja2", file=sys.stderr)
    sys.exit(1)


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

    # Get weekday name
    weekday = datetime.now().strftime("%A")

    # Render template
    template = Template(template_content)
    rendered = template.render(weekday=weekday)

    # Write output
    output_path.write_text(rendered)
    print(f"Rendered README.md with weekday: {weekday}")


if __name__ == "__main__":
    main()

