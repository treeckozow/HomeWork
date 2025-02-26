FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Copy the application code and requirements file into the container
COPY . /app

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask port
EXPOSE 5000

# Run the main application
CMD ["python", "__main__.py"]
