FROM python:3.8.3-slim-buster

CMD mkdir sih

COPY . /sih

CMD pip install flask

RUN ["python3","main.py"]
