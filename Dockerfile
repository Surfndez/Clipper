FROM python:3


RUN apt-get update
RUN apt-get install -y software-properties-common
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt install nodejs
RUN npm install twilio-cli -g
RUN npm install --unsafe-perm -g ngrok
RUN add-apt-repository -y ppa:jonathonf/ffmpeg-4
RUN apt install -y ffmpeg

WORKDIR /opt/clipper

ADD requirements.txt requirements.txt
RUN pip install  -r requirements.txt

EXPOSE 5000

COPY pyclipper .

CMD python -m pyclipper.main
