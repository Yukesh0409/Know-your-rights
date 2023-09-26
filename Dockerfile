FROM python:3.11

WORKDIR /sih

COPY . /sih

RUN pip install --upgrade pip

RUN pip install --upgrade watchdog

RUN pip install flask

RUN pip install gspread

RUN pip install pandas

RUN pip install protobuf

RUN pip install python-docx

EXPOSE 8080

CMD python ./main.py