# Use Ubuntu base image for better font support
FROM python:3.10-slim-bullseye

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info \
    fonts-dejavu \
    fonts-liberation \
    fonts-roboto \
    fontconfig \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Rebuild font cache (critical for WeasyPrint)
RUN fc-cache -f -v

# Python setup
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Collect static files (if using Whitenoise)

CMD python manage.py collectstatic --noinput && gunicorn mls.wsgi --bind 0.0.0.0:${PORT:-8000}