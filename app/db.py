import psycopg2
import time


DB_MAX_RETRIES = 3

connect_str = "dbname='postgres' user='postgres' host='database' " + \
                  "password='rowanisthebest'"

def poll_db(app):
    def poll(cur_attempts):
      try:
          conn =  psycopg2.connect(connect_str)
          app.logger.debug("Connected to database!")
          return conn
      except Exception as e:
          if (cur_attempts + 1) == DB_MAX_RETRIES:
              app.logger.error("Connection failed [%s]" % e)
              return None
          else:
            time.sleep(1)
            poll(cur_attempts + 1)
    app.logger.debug("Polling the database for TCP connection...")
    return poll(0)
