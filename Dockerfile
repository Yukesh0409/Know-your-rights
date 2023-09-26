FROM python:3.11

WORKDIR /sih

COPY . /sih


RUN pip3 install transformers

RUN pip install tensorflow --user

RUN pip install -r requirements.txt

EXPOSE 8080

CMD python ./main.py