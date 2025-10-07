FROM python:3.11

RUN apt-get update 

RUN apt-get install ffmpeg libsm6 libxext6 libmtdev-dev x11-apps -y

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

ENV DISPLAY=:0
