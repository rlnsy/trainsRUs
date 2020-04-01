from flask import Flask
from db import PSQLWrapper
from utils import ApplicationLogger

app = Flask("Trains 'R' Us")
logger = ApplicationLogger()
dbw = PSQLWrapper(logger)

@app.route('/')
def hello():
    rows = dbw.execute("""SELECT * from trains""")
    return str(rows)


if __name__ == "__main__":
    try:
      dbw.connect()
      app.run(host="0.0.0.0") # TODO change to env variable
    except Exception as e:
      logger.error("Could not set up database wrapper (see logs)")
