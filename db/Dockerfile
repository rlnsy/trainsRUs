FROM postgres:latest
ENV POSTGRES_PASSWORD rowanisthebest
COPY init/init.sh /docker-entrypoint-initdb.d/
COPY init/*.sql /docker-entrypoint-initdb.d/
