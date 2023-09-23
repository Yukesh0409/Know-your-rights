FROM python:3-alpine3.15

RUN pip install --upgrade pip

WORKDIR /application

COPY . /application

RUN pip install flask

EXPOSE 5000

CMD python ./main.py
