FROM python:3.9-slim

# Install dependencies required for Pillow and python-escpos
RUN apt-get update && apt-get install -y \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libpng-dev \
    libfreetype6-dev \
    libtiff-dev \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY cleaning_schedule.py .

# Run the script - default to scheduled mode
ENTRYPOINT ["python", "cleaning_schedule.py"]
