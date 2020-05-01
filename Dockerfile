FROM python:3

WORKDIR /opt/clipper

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt install nodejs
RUN npm install twilio-cli -g
RUN add-apt-repository -y ppa:jonathonf/ffmpeg-4
RUN apt install -y ffmpeg

ADD requirements.txt requirements.txt
RUN pip install  -r requirements.txt

EXPOSE 5000

COPY pyclipper .

CMD python -m pyclipper.main
