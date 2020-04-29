FROM python:3

WORKDIR /opt/clipper

ADD pyclipper/requirements.txt requirements.txt
RUN pip install  -r requirements.txt

EXPOSE 5000

COPY pyclipper .

CMD python -m pyclipper.main
