# syntax=docker/dockerfile:1
FROM python:3.13

# Define work directory
WORKDIR /

# Copy files
COPY . .

# Update pip & install dependencies
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

# Expose server port
EXPOSE 80

# Run server
ENTRYPOINT ["bash", "entrypoint.sh"]
