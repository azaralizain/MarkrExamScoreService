# syntax=docker/dockerfile:1

FROM python:3.8.2-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
EXPOSE 5000 3306

COPY . .

CMD [ "python3", "./MarkrExamScoreService.py"]

