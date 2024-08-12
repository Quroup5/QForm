FROM ubuntu:22.04
LABEL authors="ahmadrv"

RUN apt update && apt upgrade -y
RUN apt install -y git python3-pip curl

WORKDIR /home

RUN git clone https://github.com/Quroup5/QForm.git

WORKDIR /home/QForm/

RUN pip install -r ./requirements.txt
