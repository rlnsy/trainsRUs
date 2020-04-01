from db import PSQLWrapper
from utils import ApplicationLogger


logger = ApplicationLogger()
dbw = PSQLWrapper(logger)


def init_db_wrapper():
  """
  Initilize wrapper by testing connection
  """
  logger.info("Establishing a test connection to database")
  dbw.connect()


class MissingInput(Exception):
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
  try:
    command = r['sql']
  except KeyError:
    logger.error("Missing SQL field for execute")
    raise MissingInput("Missing SQL field")
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
