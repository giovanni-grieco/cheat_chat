# Use an official Debian as a parent image
FROM python:slim-bookworm

RUN apt-get update && apt-get install -y libpq-dev gcc
# Copy your Python application code to the container
COPY . /ccd

# Set the working directory
WORKDIR /ccd

# Create and activate a virtual environment
RUN pip install -r requirements.txt

# Expose the port your app runs on
EXPOSE 10011

CMD ["python3", "main.py"]