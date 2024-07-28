# Use Python 3.12-slim-bullseye as the base image
ARG PYTHON_VERSION=3.12-slim-bullseye
FROM python:${PYTHON_VERSION}

# Create a virtual environment and set it up
RUN python -m venv /opt/venv
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install OS dependencies for the project
RUN apt-get update && apt-get install -y \
    libpq-dev \
    libjpeg-dev \
    libcairo2 \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create the code directory and set it as the working directory
RUN mkdir -p /code
WORKDIR /code

# Copy requirements and install them
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Copy project files and CSV files into the container
COPY ./files /code/files
COPY ./src /code

# Collect static files
RUN python manage.py collectstatic --noinput

# Set the Django project name
ARG PROJ_NAME="cfehome"

# Create a bash script to run the Django project
RUN echo "#!/bin/bash\n" > ./paracord_runner.sh && \
    echo "RUN_PORT=\"\${PORT:-8000}\"\n\n" >> ./paracord_runner.sh && \
    echo "python manage.py migrate --no-input\n" >> ./paracord_runner.sh && \
    echo "gunicorn ${PROJ_NAME}.wsgi:application --bind \"0.0.0.0:\$RUN_PORT\"\n" >> ./paracord_runner.sh

# Make the bash script executable
RUN chmod +x paracord_runner.sh

# Clean up apt cache to reduce image size
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Run the Django project via the runtime script when the container starts
CMD ["./paracord_runner.sh"]
