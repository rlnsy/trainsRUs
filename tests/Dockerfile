FROM python:3.7-alpine
WORKDIR /test
RUN apk add --no-cache py-pip gcc g++ musl-dev linux-headers
RUN pip install requests
COPY . .
