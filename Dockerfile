FROM alpine:3.16
RUN mkdir /usr/src/app -p
WORKDIR /usr/src/app/
RUN apk update && apk add --no-cache bash file ffmpeg wget \
    unzip python3 py3-pip uchardet
RUN pip3 install gdown yt-dlp requests
ADD . .
RUN chmod +x makeframe.sh
CMD ./makeframe.sh
