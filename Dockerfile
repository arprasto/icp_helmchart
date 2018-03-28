# Use an official Python runtime as a parent image
FROM python:2.7-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
#RUN apt-get update
#RUN apt-get -y install gcc
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install cloudant==2.3.1
RUN pip freeze
# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
#ENV NAME Arpit
#ENV svcbindingmountpath /opt/service-bind

# Run app.py when the container launches
CMD ["python", "app.py"]
