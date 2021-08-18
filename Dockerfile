# syntax=docker/dockerfile:1
FROM python:3.8-alpine
WORKDIR /code
COPY . .
RUN pip3 install -r requirements.txt
CMD ["python3","code/MarkrExamScoreService.py"]
