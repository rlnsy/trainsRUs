from db import PSQLWrapper
from utils import ApplicationLogger


EXECUTE_TOKEN = "61YYZlA!QkeZ3V7NtY9OPDvN$u7N^E&t"
DEFAULT_LOW_ID = 1000 # To avoid conflicts with tuples from init script


logger = ApplicationLogger()
dbw = PSQLWrapper(logger)


"""
Define errors used for communication to outer layer
"""

class MissingInput(Exception):
  """
  Thrown when input to a function is missing
  require information
  """
  pass

class InputDomainError(Exception):
  """
  Thrown when input to a function is not proper
  type
  """
  pass

class NotAllowed(Exception):
  """
  Thrown when input to a function is missing
  require information
  """
  pass


"""
Useful engine helpers
"""

def init_db_wrapper():
  """
  Initilize wrapper by testing connection
  """
  logger.info("Establishing a test connection to database")
  dbw.connect()

def gen_uid(prefix):
  """
  generate a unique id within a given prefix group
  """
  logger.info("Generating UID for %s" % prefix)
  new_id = None
  records = dbw.execute("SELECT cur_id from UID WHERE prefix = '%s'" % prefix)
  if len(records) == 0:
    # no id generated
    logger.info("Prefix %s does not exist; creating" % prefix)
    new_id = DEFAULT_LOW_ID
    dbw.execute("INSERT INTO UID VALUES ('%s', %d)" % (prefix, new_id))
  else:
    # previous id within prefix
    cur_id = records[0][0]
    new_id = cur_id + 1
    dbw.execute("UPDATE UID SET cur_id = %d WHERE prefix = '%s'" % (new_id, prefix))
  logger.info("Generated ID: %d" % new_id)
  return new_id

def extract_fields(keys, input):
  """
  attempt to read values of keys from request
  raising MissingInput if unsuccessful
  """
  vals = {}
  for k in keys:
    try:
      vals[k] = input[k]
    except KeyError as ke:
      msg = ("Input missing field %s" % str(ke))
      logger.info(msg)
      raise MissingInput(msg)
  return vals



"""
Functions for sampling and debugging
"""

def sample():
  query = "SELECT * from Train"
  rows = dbw.execute(query)
  return {
    'executed': query,
    'tuples': str(rows),
    'message': "This is an example of what you can execute on the database!"
  }

def handle_execute(i):
  v = extract_fields(['sql', 'ex_token'], i)
  if v['ex_token'] != EXECUTE_TOKEN:
    raise NotAllowed("Invalid execute token")
  try:
    result = dbw.execute(v['sql'])
    return {
      'executed': v['sql'],
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


"""
Create worker
"""

new_worker_tables = {
  'Train': "Train_Worker" ,
  'Maintenance': "Maintenance_Worker",
  'Station': "Station_Worker"
}

def create_worker(i):
  v = extract_fields([
    'firstName', 'lastName', 'phoneNumber', 'role',
    'availability', 'workerType'
  ], i)
  if v['workerType'] not in new_worker_tables:
    raise InputDomainError("Invalid worker type")
  wid = gen_uid('worker')
  dbw.execute((
    """
    INSERT INTO Worker VALUES (%d, '%s', '%s', '%s', '%s', '%s');
    """
    % (wid, 
    v['firstName'], 
    v['lastName'], 
    v['phoneNumber'], 
    v['role'], 
    v['availability'])))
  dbw.execute((
    """
    INSERT INTO %s (worker_id) VALUES (%d);
    """
    % (new_worker_tables[v['workerType']], wid)))
  return {
  'workerId': wid
  }
