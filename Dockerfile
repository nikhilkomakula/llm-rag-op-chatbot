FROM python:3.11.5-slim

# Set the working directory to /code
WORKDIR /code

# Copy requirements.txt to working directory
COPY requirements.txt ./

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# install git & git-lfs
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get install -y git-lfs

# Expose the secret SECRET_EXAMPLE at buildtime and use its value to clone the repo
RUN --mount=type=secret,id=HUGGINGFACEHUB_API_TOKEN,mode=0444,required=true \
    git clone --depth 1 https://nikhilkomakula:$(cat /run/secrets/HUGGINGFACEHUB_API_TOKEN)@huggingface.co/spaces/nikhilkomakula/llm-rag-op-chatbot3 /code/llm-rag-op-chatbot3

# Set up a new user named "user" with user ID 1000
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set home to the user's home directory
ENV HOME=/home/user \
	PATH=/home/user/.local/bin:$PATH

# Set the working directory to the user's home directory
WORKDIR $HOME/app

# Copy the files/folders into the container at $HOME/app setting the owner to the user
COPY --chown=user app.py $HOME/app
COPY --chown=user src $HOME/app/src
COPY --chown=user indexes $HOME/app/indexes

# Use ENTRYPOINT to specify the command to run when the container starts
ENTRYPOINT ["python", "app.py"]

# Download LFS files
RUN echo "Downloading LFS files..." && \
    cd /code/llm-rag-op-chatbot3/indexes && \
    git lfs pull

