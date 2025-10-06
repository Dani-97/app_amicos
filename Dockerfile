FROM ubuntu:25.04

RUN apt-get update
RUN apt-get install nano -y
RUN apt-get install python3.13-venv -y
RUN apt-get install python3-pip -y

WORKDIR /app

RUN python3 -m venv dev_env

ENV PATH="/app/dev_env/bin:$PATH"

COPY . .

RUN pip3 install -r ./src/requirements.txt
