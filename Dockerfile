# Use the official Python image
FROM python:3.11

# Set working directory
WORKDIR /app

# Install system dependencies (required for WeasyPrint)
RUN apt update && apt install -y \
    libpangocairo-1.0-0 \
    libcairo2 \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run migrations
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8080

# Run Gunicorn server
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "mls.wsgi:application"]
