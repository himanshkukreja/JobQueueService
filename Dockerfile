# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

RUN mkdir -p /var/log

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install Python dependencies
RUN pip install -r requirements.txt

# Install Supervisor
RUN apt-get update && apt-get install -y supervisor

# Supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf


#Set environment variables from build arguments

ARG AWS_ACCESS_KEY_ID
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}

ARG AWS_SECRET_ACCESS_KEY
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}

ENV AWS_DEFAULT_REGION ap-south-1


# Run Supervisor when the container starts
CMD ["/usr/bin/supervisord"]