FROM python:3.11-slim

WORKDIR /workspace

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy project files and install dependencies using uv
COPY pyproject.toml .
RUN uv pip install --system .

# Copy render script
COPY render_readme.py .

# Default command
ENTRYPOINT ["python", "render_readme.py"]

