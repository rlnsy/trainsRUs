import psycopg2
import time
from utils import trim_char_seq as trim
from decimal import Decimal


"""
Define errors
"""

class ConnectionError(Exception):
  """
  Thrown when a database transaction cannot be started
  """
  def __init__(self):
    super(ConnectionError, self).__init__("Can't connect to database")

class EmptyQueryError(Exception):
  """
  Thrown when input to database execute is empty
  """
  def __init__(self):
    super(EmptyQueryError, self).__init__("Can't execute an empty query, silly")

class DBExecuteError(Exception):
  """
  Encapsulates a formatted version of the built-in driver error messages
  We allow internal driver messages to propogate through for the time being,
  with the exception of EmptyQueryError
  """
  def __init__(self, derror):
    msg = str(derror).replace("\"", "'").replace("\n", "; ").rstrip('^; ')
    super(DBExecuteError, self).__init__(msg)


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
    self._logger_ = logger

  def _log_(self, l, msg):
    """
    Logger function
    """
    l("[DBWRAPPER] %s" % msg)

  def _format_results_(self, dbresult):
    """
    Convert DB driver results into readable string results
    """
    if type(dbresult) is tuple:
      data = ""
      for i in range(0, len(dbresult)):
        val = dbresult[i]
        if type(val) is str:
          data += "'%s' " % trim(val)
        elif type(val) is bool:
          data += "%s " % ("true" if val else "false")
        elif val is None:
          data += "NULL "
        elif type(val) is Decimal:
          data += "%f " % float(val)
        else:
          data += "%s " % val
      return data
    elif type(dbresult is list):
      if len(dbresult) == 0:
        return """
      No results
        """
      else:
        results = ""
        for i,r in enumerate(dbresult):
          if i > 0:
            results += "      "
          results += "%d. (%s)\n" % (i + 1, self._format_results_(r))
        return """
      %s
        """ % results
    else:
      return str(dbresult)
  
  def connect(self):
    """
    Attempts to connect to the database.
    Pollling is only put in place in case a connection attempt is made
    while the appliction is available externally but the underlying db
    is not yet started
    """
    def poll(cur_attempts):
      try:
          conn =  psycopg2.connect(DB_CONNECT_STR)
          self._log_(self._logger_.info, "Connected!")
          return conn
      except Exception as e:
          if (cur_attempts + 1) == DB_MAX_CONNECTION_RETRIES:
              self._log_(
                self._logger_.error, "Connection failed")
              raise Exception("Could not connect")
          else:
            self._log_(
                self._logger_.warn, "Connection failed: %s" % str(e))
            time.sleep(1)
            return poll(cur_attempts + 1)
    self._log_(
      self._logger_.info, 
      "Polling the database for TCP connection...")
    return poll(0)


  def execute(self, sql):
    transaction = None
    try:
      transaction = self.connect()
    except Exception:
      raise ConnectionError()
    if len(sql) == 0:
      self._log_(self._logger_.warn, "Empty query")
      raise EmptyQueryError()
    else:
      try:
        self._log_(self._logger_.info, "%s" % sql)
        self._log_(self._logger_.demo, "SQL:\n%s" % sql)
        cursor = transaction.cursor()
        cursor.execute(sql)
        transaction.commit()
        try:
          result = cursor.fetchall()
        except Exception:
          # command is essentially void return type e.g. INSERT
          self._log_(self._logger_.demo, "Results: N/A")
          return None
        self._log_(self._logger_.demo, "Results:\n%s" % self._format_results_(result))
        return result
      except Exception as de:
        self._log_(self._logger_.warn, "Execute error: %s" % str(de))
        raise DBExecuteError(de)
      finally:
        self._log_(self._logger_.debug, "Closing cursor")
        cursor.close()
        self._log_(self._logger_.debug, "Closing transaction")
        transaction.close()
