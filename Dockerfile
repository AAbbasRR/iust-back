# Use a minimal base image
FROM python:3.10-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gettext \
    libpq-dev \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY ./requirements.txt /app/requirements.txt
# Install any needed dependencies specified in requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY ./src /app
COPY ./.env /app/src/.env

# Expose the port that Gunicorn will listen on
EXPOSE 8000

# Start Gunicorn to serve the Django application
CMD ["gunicorn", "Abrat.wsgi:application", "--bind", "0.0.0.0:8000"]
