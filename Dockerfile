FROM python:3.9-slim

# Install dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0

# Set the working directory
WORKDIR /app

# Copy the app files into the container
COPY . /app

# Install Python dependencies
RUN pip install -r requirements.txt

# Expose the port the app will run on
EXPOSE 5000

# Run the application
CMD ["flask", "run", "--host=0.0.0.0"]
