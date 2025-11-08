# Use official Python base image
FROM python:3.12

# Set working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install dependencies in editable mode
RUN pip install --no-cache-dir -e .

# Expose Flask default port
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=app.py

# Run the Flask application
CMD ["python", "app.py"]