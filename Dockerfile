FROM python:3-alpine3.15
WORKDIR /application
COPY . /application
RUN pip install flask
EXPOSE 5000
CMD python ./main.py
