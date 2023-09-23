FROM python:3-alpine3.15
 
RUN pip install --upgrade pip

WORKDIR /sih

COPY . /sih

RUN pip install flask

EXPOSE 8080

CMD python ./main.py
