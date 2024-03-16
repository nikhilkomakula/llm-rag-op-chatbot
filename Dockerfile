FROM python:3.11.5-slim

RUN useradd -m -u 1000 user
USER user

WORKDIR /app

RUN chown -R user:user /app

# Copy the application files into the container
COPY --chown=user:user requirements.txt /app/
COPY --chown=user:user app.py /app/

# Install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY --chown=user:user src /app/src
COPY --chown=user:user indexes /app/indexes

# Expose the port on which your application runs inside the container
EXPOSE 7860

# Use ENTRYPOINT to specify the command to run when the container starts
ENTRYPOINT ["python", "app.py"]
