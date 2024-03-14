FROM python:3.11.5-slim

WORKDIR /app

COPY app.py requirements.txt /app/
COPY src /app/src
COPY indexes /app/indexes

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Use ENTRYPOINT to specify the command to run when the container starts
ENTRYPOINT ["python", "app.py"]
