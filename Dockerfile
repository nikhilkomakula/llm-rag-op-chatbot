FROM python:3.11.5-slim

# Set the working directory to /code
WORKDIR /code

# Copy requirements.txt to working directory
COPY requirements.txt /code/

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# install git & git-lfs
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Clone the Git repo 
RUN git clone --depth 1 -b deploy-to-hf-spaces https://github.com/nikhilkomakula/llm-rag-op-chatbot.git $HOME/app

# Use ENTRYPOINT to specify the command to run when the container starts
ENTRYPOINT ["python", "gradio_app.py"]
