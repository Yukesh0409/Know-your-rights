FROM pypy:3

WORKDIR /sih

COPY . /sih

RUN pip install transformers

RUN pip install tensorflow --user

RUN pip install -r requirements.txt

EXPOSE 8080

CMD python ./main.py