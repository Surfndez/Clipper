FROM python:3

WORKDIR /opt/clipper

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:jonathonf/ffmpeg-4
RUN apt install -y ffmpeg

ADD requirements.txt requirements.txt
RUN pip install  -r requirements.txt

EXPOSE 5000

COPY pyclipper .

CMD python -m pyclipper.main
