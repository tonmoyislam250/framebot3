FROM alpine:3.16

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app/

# Install dependencies
RUN apk update && apk add --no-cache bash file ffmpeg wget \
    unzip python3 py3-pip uchardet

# Install Python packages
RUN pip3 install gdown yt-dlp requests python-dotenv flask

# Copy source code
ADD . .

# Ensure scripts are executable
RUN chmod +x frame.sh

# Expose port for Render/Heroku/etc.
EXPOSE 8080

# Run Flask app (which calls your script)
CMD ["python3", "server.py"]
