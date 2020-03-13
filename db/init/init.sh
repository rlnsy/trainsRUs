#!/bin/bash
set -e

# Currently this user does nothing because I don't know how to set the password
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname postgres <<-EOSQL
    CREATE USER trainsrus;
    GRANT ALL PRIVILEGES ON DATABASE postgres TO trainsrus;
EOSQL
