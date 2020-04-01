import psycopg2
import time


"""
Define database constants
"""
DB_MAX_CONNECTION_RETRIES = 3
DB_CONNECT_STR =  "dbname='postgres' "  + \
                  "user='postgres' "    + \
                  "host='database' "    + \
                  "password='rowanisthebest'"


class PSQLWrapper:
  """
  An abstraction over the local database to allow SQL queries to be executed 
  easily
  """

  def __init__(self, logger):
    """
    Initialize a wrapper instance with a null connection and a reference
    to the main application logger
    """
    self._connection_ = None # contains the single db connection instance
    self._logger_ = logger

  def is_connected(self):
    """
    Determine whether the wrapper is connected to the database
    """
    return (self._connection_ is not None)

  def _log_(self, l, msg):
    """
    Logger function
    """
    l("[DBWRAPPER] %s" % msg)
  
  def connect(self):
    """
    Attempts to connect to the database.
    """
    if self.is_connected():
      raise Exception("Database connection already exists")
    else:
      def poll(cur_attempts):
        try:
            self._connection_ =  psycopg2.connect(DB_CONNECT_STR)
            self._log_(self._logger_.info, "Connected to database!")
        except Exception as e:
            if (cur_attempts + 1) == DB_MAX_CONNECTION_RETRIES:
                self._log_(
                  self._logger_.error, "Connection failed")
                raise Exception("Could not connect to database")
            else:
              time.sleep(1)
              poll(cur_attempts + 1)
      self._log_(
        self._logger_.info, 
        "Polling the database for TCP connection...")
      poll(0)

  def close(self):
    """
    Close connection to DB
    """
    self._connection_.close()

  def execute(self, sql):
    self._log_(self._logger_.info, "%s" % sql)
    cursor = self._connection_.cursor()
    cursor.execute(sql)
    self._connection_.commit()
    result = cursor.fetchall()
    cursor.close()
    return result
