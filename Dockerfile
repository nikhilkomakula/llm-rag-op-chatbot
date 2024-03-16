FROM python:3.11.5-slim

WORKDIR /app

# Create a cache directory and grant permissions
RUN mkdir /.cache && chmod -R 777 /.cache

# Copy the application files into the container
COPY app.py requirements.txt /app/
COPY src /app/src
COPY indexes /app/indexes

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose the port on which your application runs inside the container
EXPOSE 7860

# Use ENTRYPOINT to specify the command to run when the container starts
ENTRYPOINT ["python", "app.py"]
