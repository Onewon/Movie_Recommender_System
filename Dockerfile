# Use an official Python runtime as a base image
FROM python:3.5

# Set PYTHONUNBUFFERED so output is displayed in the Docker log
ENV PYTHONUNBUFFERED=1

# Make port 80 available to the world outside this container
EXPOSE 8000
# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# update pip resource
COPY pip.conf /etc/pip.conf
# Install dependencies
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy the rest of the application's code
# COPY . /usr/src/app

# Run the app
CMD ["./run_app.sh"]
