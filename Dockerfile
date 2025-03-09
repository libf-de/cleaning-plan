FROM python:3.9-slim

WORKDIR /app

# Install required packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY cleaning_schedule.py .

# Run the script - default to scheduled mode
ENTRYPOINT ["python", "cleaning_schedule.py"]
