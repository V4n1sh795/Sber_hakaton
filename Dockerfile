# Use a slim Python image as the base
FROM python:3.11-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project files
COPY . .

# Expose the port where the application will run
EXPOSE 8000

# Command to run the Django application (e.g., using Gunicorn)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mysite.wsgi:application"]