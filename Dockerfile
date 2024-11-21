FROM python:3.10
RUN pip install --upgrade pip
RUN mkdir /app

COPY ./requirements.txt /app

COPY ./pageloot_project /app
WORKDIR /app/

RUN pip install -r requirements.txt
