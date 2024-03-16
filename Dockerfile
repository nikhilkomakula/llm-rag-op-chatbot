FROM python:3.11.5-slim

# Set the working directory to /code
WORKDIR /code

# Copy requirements.txt to working directory
COPY requirements.txt ./

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# install git & git-lfs
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git && \
    apt-get install -y git-lfs

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

# Copy git lfs files
RUN git clone --no-checkout --depth 1 https://huggingface.co/spaces/nikhilkomakula/llm-rag-op-chatbot
RUN cd $HOME/app/indexes && git lfs pull -I "indexes/chroma.sqlite3"
RUN cd $HOME/app/indexes/c607d7bb-5476-4bdc-8df3-36895a74111c && git lfs pull -I "indexes/c607d7bb-5476-4bdc-8df3-36895a74111c/data_level0.bin"

# Use ENTRYPOINT to specify the command to run when the container starts
ENTRYPOINT ["python", "app.py"]
