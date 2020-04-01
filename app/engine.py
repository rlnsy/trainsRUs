from db import PSQLWrapper
from utils import ApplicationLogger


EXECUTE_TOKEN = "61YYZlA!QkeZ3V7NtY9OPDvN$u7N^E&t"


logger = ApplicationLogger()
dbw = PSQLWrapper(logger)


def init_db_wrapper():
  """
  Initilize wrapper by testing connection
  """
  logger.info("Establishing a test connection to database")
  dbw.connect()

"""
Define errors used for communication
"""

class MissingInput(Exception):
  """
  Thrown when input to a function is missing
  require information
  """
  pass

class NotAllowed(Exception):
  """
  Thrown when input to a function is missing
  require information
  """
  pass


def sample():
  query = "SELECT * from trains"
  rows = dbw.execute(query)
  return {
    'executed': query,
    'tuples': str(rows),
    'message': "This is an example of what you can execute on the database!"
  }


def handle_execute(r):
  command = ""
  token = "" 
  try:
    command = r['sql']
    token = r['ex_token']
  except KeyError as ke:
    msg = ("Missing field %s for execute" % str(ke))
    logger.info(msg)
    raise MissingInput(msg)
  if token != EXECUTE_TOKEN:
    raise NotAllowed("Invalid execute token")
  try:
    result = dbw.execute(command)
    return {
      'executed': command,
      'result': str(result)
    }
  except Exception as e:
    return {
      'attempted': None,
      'error': {
        'message': "Error executing SQL",
        'cause': str(e)
      }
    }
