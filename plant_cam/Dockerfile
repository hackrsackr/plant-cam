# We use the official `python` image as base.
# FROM python:3.12-slim

# Copy the python script into the image
# Syntax: `COPY [SOURCE] [DESTINATION]`
# COPY script.py /app/script.py

# We need to run commands while building the image
# This will install the `requests` package so we can use it in script.py
# RUN apt update; apt install -y libgl1
# RUN pip install opencv-python

# The command is executed when the container starts
# CMD ["python3", "-u", "/app/take_pictures.py"]


# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the container
COPY src/take_pictures.py /app/take_pictures.py
COPY requirements.txt /app

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
# ENV NAME World

# Run app.py when the container launches
CMD ["python", "take_pictures.py"]