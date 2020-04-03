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

class NotFound(Exception):
  """
  Thrown when a requested instance of a resource
  is not found
  """
  pass

class HandlerNotImplemented(Exception):
  """
  Thrown when a requested function is not
  implemented
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

def trim_char_seq(s):
  if s is None:
    return None
  elif type(s) is not str:
    logger.error("String trim received %s" % str(s))
    raise Exception("Invalid type for char strip: %s" % str(type(s)))
  return s.rstrip(' ')


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


WORKER_TABLES = {
  'Train': "Train_Worker" ,
  'Maintenance': "Maintenance_Worker",
  'Station': "Station_Worker"
}

WORKER_FIELDS = [
    'firstName', 'lastName', 'phoneNumber', 'role',
    'availability', 'workerType'
]


"""
Create worker
"""

def create_worker(i):
  v = extract_fields(WORKER_FIELDS, i)
  if v['workerType'] not in WORKER_TABLES:
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
    % (WORKER_TABLES[v['workerType']], wid)))
  return {
  'workerId': wid
  }


"""
Remove worker
"""

def remove_worker(i):
  v = extract_fields(['workerId'], i)
  if type(v['workerId']) is not int:
    raise InputDomainError()
  search = dbw.execute("SELECT * FROM Worker WHERE id=%d" % v['workerId'])
  if len(search) == 0:
    raise NotFound("Worker %d does not exist" % v['workerId'])
  dbw.execute("DELETE FROM Worker WHERE id=%d" % v['workerId'])
  return {
    'message': 'success'
  }


"""
Get worker
"""

def get_single_worker(i, target_worker_type=None):
  v = extract_fields(['workerId'], i)
  if type(v['workerId']) is not int:
    raise InputDomainError()
  match = None
  worker_type = None
  for t in WORKER_TABLES:
    table = WORKER_TABLES[t]
    search = dbw.execute(
    """
    SELECT
    * 
    FROM
      Worker INNER JOIN %s
      ON %s.worker_id = Worker.id
    WHERE
      Worker.id = %d;
    """
    % (table, table, v['workerId']))
    if len(search) != 0:
      match = search[0]
      worker_type = t
      break
  if match is None:
    raise NotFound("Worker %d does not exist" % v['workerId'])
  else:
    if ((worker_type != target_worker_type) and 
        (target_worker_type is not None)):
      raise NotFound(
    "Worker %d is not of type %s" % (v['workerId'], target_worker_type))
    return {
      'firstName': trim_char_seq(match[1]),
      'lastName': trim_char_seq(match[2]),
      'phoneNumber': trim_char_seq(match[3]),
      'role': trim_char_seq(match[4]),
      'availability': trim_char_seq(match[5]),
      'workerType': worker_type
    }


"""
Update worker
"""

def update_worker(i):
  wid = extract_fields(['workerId'], i)['workerId']
  worker_data = get_single_worker({'workerId': wid})
  n_updates = 0
  for key in i:
    if key != 'workerId':
      if key not in WORKER_FIELDS:
        raise InputDomainError
      else:
        n_updates += 1
        worker_data[key] = i[key]
  if n_updates == 0:
    raise MissingInput("Request contains no updates")
  command = (
    """
    UPDATE Worker
    SET
    first_name = '%s',
    last_name = '%s',
    phone_number = '%s',
    role_name = '%s',
    availability = '%s'
    WHERE id = '%d'
    """ % (
    worker_data['firstName'],
    worker_data['lastName'],
    worker_data['phoneNumber'],
    worker_data['role'],
    worker_data['availability'],
    wid))
  try:
    dbw.execute(command)
  except TypeError as te:
    raise InputDomainError(str(te))
  return {
    'message': 'success'
  }


"""
Get segments
"""

def get_segments(i):
  wid = None
  if 'workerId' in i:
    wid = i['workerId']
  data = []
  query = None
  if wid is None:
    query = "SELECT id, condition FROM Segment;"
  else:
    query = ("""
    SELECT
      id, condition
    FROM
      Segment INNER JOIN Works_On
      ON Works_On.segment_id = Segment.id
    WHERE
      Works_On.maintenance_worker_id = %d;
    """ % wid)
  for t in dbw.execute(query):
    data.append({
      'segmentId': t[0],
      'status': trim_char_seq(t[1])
    })
  return data


"""
Create segment
"""

def create_segment(i):
  v = extract_fields(
    ['trackLength', 'condition', 'startStation', 'endStation'], i)
  sid = gen_uid('segment')
  dbw.execute((
    """
    INSERT INTO Segment VALUES (%d, '%d', '%s', '%s', '%s');
    """
    % (sid, 
    v['trackLength'], 
    v['condition'], 
    v['startStation'], 
    v['endStation'])))
  return {
    'message': "Segment created",
    'segmentId': sid
  }


"""
Get Segment info
"""

def get_segment_info(i):
  v = extract_fields(['segmentId'], i)
  if type(v['segmentId']) is not int:
    raise InputDomainError()
  search = dbw.execute(
    """
    SELECT * FROM Segment WHERE id = %d;
    """ % v['segmentId']) 
  if len(search) == 0:
    raise NotFound("Segment %d does not exist" % v['segmentId'])
  else:
    match = search[0]
    return {
    'trackLength': match[1],
    'condition': trim_char_seq(match[2]),
    'startStation': trim_char_seq(match[3]),
    'endStation': trim_char_seq(match[4])
  }


"""
Update Segment status
"""

def update_segment(i):
  v = extract_fields(['segmentId', 'newStatus'], i)
  get_segment_info({ 'segmentId': v['segmentId'] })
  dbw.execute(
    """
    UPDATE Segment SET condition = '%s' WHERE id = %d;
    """ % (v['newStatus'], v['segmentId']))
  return {
    'message': 'Segment updated'
  }


"""
Get worker shifts
"""

def get_worker_shifts(i):
  v = extract_fields(['workerId'], i)
  wid = v['workerId']
  results = []
  for r in dbw.execute(
    """
    SELECT * from Works_Shift
    WHERE train_worker_id = %d
    """ % wid):
    results.append({
      'tripId': r[1],
      'segmentId': r[2],
      'numHours': r[3],
      'startTime': trim_char_seq(r[4])
    })
  return results


"""
Schedule worker shift
"""

def get_trip_info(i):
  v = extract_fields(['tripId'], i)
  if type(v['tripId']) is not int:
    raise InputDomainError()
  search = dbw.execute(
    """
    SELECT * FROM Trip WHERE id = %d;
    """ % v['tripId']) 
  if len(search) == 0:
    raise NotFound("Trip %d does not exist" % v['tripId'])
  else:
    match = search[0]
    return {
    'departureTime': trim_char_seq(match[1]),
    'arrivalTime': trim_char_seq(match[2])
  }

def schedule_shift(i):
  v = extract_fields(
    [
      'workerId', 'tripId', 'segmentId', 
      'numHours', 'startTime'
    ], i)
  get_segment_info(v)
  get_single_worker(v, target_worker_type='Train')
  get_trip_info(v)
  search = dbw.execute(
    """
    SELECT * FROM Works_Shift 
    WHERE 
      train_worker_id = %d
      AND
      trip_id = %d
      AND
      segment_id = %d
    """ % (v['workerId'], v['tripId'], v['segmentId']))
    # TODO: create a get shift helper
  if len(search) > 0:
    raise NotAllowed("Shift already exists and you cannot add it again")
  dbw.execute((
    """
    INSERT INTO Works_Shift VALUES (%d, '%d', '%d', '%d', '%s');
    """
    % (v['workerId'], 
    v['tripId'], 
    v['segmentId'], 
    v['numHours'], 
    v['startTime'])))
  return {
    'message': "Shift created"
  }


"""
Remove worker shift
"""

def remove_shift(i):
  v = extract_fields(
    [
      'workerId', 'tripId', 'segmentId'
    ], i)
  search = dbw.execute(
    """
    SELECT * FROM Works_Shift 
    WHERE 
      train_worker_id = %d
      AND
      trip_id = %d
      AND
      segment_id = %d
    """ % (v['workerId'], v['tripId'], v['segmentId']))
    # TODO: create a get shift helper
  if len(search) == 0:
    raise NotFound("Requested shift does not exist")
  dbw.execute(
    """
    DELETE FROM Works_Shift 
    WHERE 
      train_worker_id = %d
      AND
      trip_id = %d
      AND
      segment_id = %d
    """ % (v['workerId'], v['tripId'], v['segmentId']))
  return {
    'message': "Shift deleted"
  }


"""
Get ticket info
"""

def get_passenger_info(i):
  v = extract_fields(['passengerId'], i)
  if type(v['passengerId']) is not int:
    raise InputDomainError()
  search = dbw.execute(
    """
    SELECT * FROM Passenger WHERE id = %d;
    """ % v['passengerId'])
  if len(search) == 0:
    raise NotFound("Passenger %d does not exist" % v['passengerId'])
  else:
    match = search[0]
    return {
      'passengerId': v['passengerId'],
      'name': ("%s %s" % (trim_char_seq(match[1]), trim_char_seq(match[2]))),
      'phoneNumber': trim_char_seq(match[3]),
      'email': trim_char_seq(match[4])
    }

def get_class_info(i):
  v = extract_fields(['classType'], i)
  search = dbw.execute(
    """
    SELECT * FROM Class WHERE type = '%s';
    """ % v['classType'])
  if len(search) == 0:
    raise NotFound("Class %s does not exist" % v['classType'])
  else:
    match = search[0]
    return {
      'classType': trim_char_seq(match[0]),
      'refundable': match[1],
      'priorityBoarding': match[2],
      'freeFood': match[3]
    }

def get_ticket_info(i):
  v = extract_fields([
    'tripId', 'seatNumber'
  ], i)
  search = dbw.execute(
    """
    SELECT * FROM Ticket
    WHERE 
      seat_number = %d
      AND
      trip_id = %d
    """ % (v['seatNumber'], v['tripId']))
  if len(search) == 0:
    raise NotFound("Requested ticket does not exist")
  else:
    match = search[0]
    pid = match[1]
    ctype = match[2]
    passenger = get_passenger_info({'passengerId': pid})
    ticketclass = get_class_info({'classType': ctype})
    return {
      'seatNumber': match[0],
      'passenger': passenger,
      'class': ticketclass
    }


"""
Station stuff
"""

def create_station(i):
  raise HandlerNotImplemented()

def get_station(i):
  raise HandlerNotImplemented()

def update_station(i):
  raise HandlerNotImplemented()

