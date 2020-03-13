FROM python:3.7-alpine
WORKDIR /trainsrus
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache py-pip postgresql-dev gcc g++ musl-dev linux-headers
RUN pip install flask
RUN pip install psycopg2
COPY app .
