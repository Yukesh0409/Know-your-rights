FROM python:3.8.3-slim-buster

COPY . /src

CMD pip install flask

RUN ["python3","main.py"]
