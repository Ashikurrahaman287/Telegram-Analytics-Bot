# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable for bot token
ENV TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"

# Run the bot when the container launches
CMD ["python", "telegram_bot.py"]
