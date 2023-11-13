# Use the official Python image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy your Python server code into the container
COPY run.py /app/run.py

# Expose the port your server will listen on
EXPOSE 12345

# Run your Python server when the container starts
CMD ["python", "run.py"]
