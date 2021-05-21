# Use the Python3.7.8 image
FROM python:3.7.8-buster

# Set the working directory to /app
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the current directory contents into the container at /app
ADD . /app

# Install the dependencies
RUN pip install -r requirements.txt

EXPOSE 8080

# run the command to start uWSGI
CMD ["uwsgi", "app.ini"]