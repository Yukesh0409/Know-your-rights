FROM python:3.8.3-slim-buster

COPY . .

CMD pip install flask

RUN ["python","main.py"]
