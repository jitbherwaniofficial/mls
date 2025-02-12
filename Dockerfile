FROM python:3.9-slim

# Install WeasyPrint system dependencies
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    shared-mime-info

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files (if using Whitenoise)

CMD python manage.py collectstatic --noinput && gunicorn mls.wsgi --bind 0.0.0.0:${PORT:-8000}