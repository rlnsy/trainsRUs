from db import PSQLWrapper
from utils import ApplicationLogger, trim_char_seq as trim, loadAuthToken


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


class Engine:

  def __init__(self, app_logger):
    """ init logger """
    self._logger = app_logger
    """ Initilize wrapper and test connection """
    self._dbw = PSQLWrapper(app_logger)
    self._logger.info("Establishing a test connection to database")
    self._dbw.connect()
    self.EXECUTE_TOKEN = loadAuthToken()
    self._logger.info("Loaded authorization token: %s" % self.EXECUTE_TOKEN)


  """
  Useful engine helpers
  """

  def gen_uid(self, prefix):
    """
    generate a unique id within a given prefix group
    """
    self._logger.info("Generating UID for %s" % prefix)
    new_id = None
    records = self._dbw.execute(
      """
      SELECT cur_id from UID WHERE prefix = '%s'
      """ % prefix)
    if len(records) == 0:
      """
      no id generated
      this suggests that no tuples of the form (<prefix>, _) 
      exist in UID table
      """
      self._logger.info("Prefix %s does not exist; creating" % prefix)
      new_id = 0 # create the first id, 0
      self._dbw.execute(
        """
      INSERT INTO UID VALUES ('%s', %d)
        """ % (prefix, new_id))
    else:
      # previous id within prefix
      cur_id = records[0][0]
      new_id = cur_id + 1
      self._dbw.execute(
        """
      UPDATE UID SET cur_id = %d WHERE prefix = '%s'
        """ % (new_id, prefix))
    self._logger.info("Generated ID: %d" % new_id)
    return new_id

  def extract_fields(self, keys, input):
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
        self._logger.info(msg)
        raise MissingInput(msg)
    return vals


  """
  Functions for sampling and debugging
  """

  def sample(self):
    query = """
      SELECT * from Train
      """
    rows = self._dbw.execute(query)
    return {
      'executed': query,
      'tuples': str(rows),
      'message': "This is an example of what you can execute on the database!"
    }

  def handle_execute(self, i):
    v = self.extract_fields(['sql', 'ex_token'], i)
    if v['ex_token'] != self.EXECUTE_TOKEN:
      raise NotAllowed("Invalid execute token")
    try:
      result = self._dbw.execute(
        """
        %s
        """ % v['sql'])
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

  def create_worker(self, i):
    v = self.extract_fields(self.WORKER_FIELDS, i)
    if v['workerType'] not in self.WORKER_TABLES:
      raise InputDomainError("Invalid worker type")
    wid = self.gen_uid('worker')
    self._dbw.execute((
      """
      INSERT INTO Worker VALUES (%d, '%s', '%s', '%s', '%s', '%s');
      """
      % (wid, 
      v['firstName'], 
      v['lastName'], 
      v['phoneNumber'], 
      v['role'], 
      v['availability']))) # Q.1
    self._dbw.execute((
      """
      INSERT INTO %s (worker_id) VALUES (%d);
      """
      % (self.WORKER_TABLES[v['workerType']], wid))) # Q.2
    return {
    'workerId': wid
    }


  """
  Remove worker
  """

  def remove_worker(self, i):
    v = self.extract_fields(['workerId'], i)
    if type(v['workerId']) is not int:
      raise InputDomainError()
    search = self._dbw.execute(
      """
      SELECT * FROM Worker
      WHERE id=%d
      """ % v['workerId'])
    if len(search) == 0:
      raise NotFound("Worker %d does not exist" % v['workerId'])
    self._dbw.execute(
      """
      DELETE FROM Worker
      WHERE id=%d
      """ % v['workerId']) # Q.3
    return {
      'message': 'success'
    }


  """
  Get worker
  """

  W_ATTR = {
    'workerId': 'id',
    'firstName': 'first_name',
    'lastName': 'last_name',
    'phoneNumber': 'phone_number',
    'role': 'role_name',
    'availability': 'availability'
  }

  def get_single_worker(self, i, target_worker_type=None):
    """
    Gets a single worker, or many if no id is specified.
    Supports field projection.
    """
    if 'workerId' in i:
      v = self.extract_fields(['workerId'], i)
      if type(v['workerId']) is not int:
        raise InputDomainError()
      fields = []
      if 'fields' in i:
        if type(i['fields']) is not list:
          raise InputDomainError("Fields must be a list")
        for f in i['fields']:
          if f != 'workerType':
            if f not in self.W_ATTR:
              raise InputDomainError("Field %s is not valid for Worker" % str(f))
            else:
              fields.append(f)
      else:
        fields = self.W_ATTR.keys()
      attr_selection = ",".join([self.W_ATTR[f] for f in fields])
      match = None
      worker_type = None
      for t in self.WORKER_TABLES:
        table = self.WORKER_TABLES[t]
        search = self._dbw.execute(
        """
      SELECT
      %s 
      FROM
        Worker INNER JOIN %s
        ON %s.worker_id = Worker.id
      WHERE
        Worker.id = %d;
        """
        % (attr_selection, table, table, v['workerId'])) # Q.8
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
        result = {}
        for j, f in enumerate(fields):
          val = match[j]
          if type(val) is str:
            result[f] = trim(val)
          else:
            result[f] = val
        if ('fields' in i) and ('workerType' in i['fields']) or ('fields' not in i):
          result['workerType'] = worker_type
        return result
    else:
      # All workers case
      search = self._dbw.execute(
        """
      SELECT * FROM Worker;
        """)
      results = []
      for w in search:
        wid = w[0]
        if 'fields' in i:
          results.append(self.get_single_worker({'workerId': wid, 'fields': i['fields']}))
        else:
          results.append(self.get_single_worker({'workerId': wid}))
      return results


  """
  Update worker
  """

  def update_worker(self, i):
    wid = self.extract_fields(['workerId'], i)['workerId']
    worker_data = self.get_single_worker({'workerId': wid})
    n_updates = 0
    for key in i:
      if key != 'workerId':
        if key not in self.WORKER_FIELDS:
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
      self._dbw.execute(command)
    except TypeError as te:
      raise InputDomainError(str(te))
    return {
      'message': 'success'
    }


  """
  Get segments
  """

  def get_segments(self,i):
    wid = None
    if 'workerId' in i:
      wid = i['workerId']
    data = []
    query = None
    if wid is None:
      query = """
      SELECT * FROM Segment;
      """
    else:
      query = ("""
      SELECT
        *
      FROM
        Segment INNER JOIN Works_On
        ON Works_On.segment_id = Segment.id
      WHERE
        Works_On.maintenance_worker_id = %d;
      """ % wid) # Q.9
    for t in self._dbw.execute(query):
      data.append({
        'segmentId': t[0],
        'trackLength': t[1],
        'condition': trim(t[2]),
        'startStation': trim(t[3]),
        'endStation': trim(t[4])
      })
    return data


  """
  Create segment
  """

  def create_segment(self, i):
    v = self.extract_fields(
      ['trackLength', 'condition', 'startStation', 'endStation'], i)
    sid = self.gen_uid('segment')
    self._dbw.execute((
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

  def get_segment_info(self, i):
    if 'segmentId' in i:
      if type(i['segmentId']) is not int:
        raise InputDomainError()
      search = self._dbw.execute(
        """
      SELECT * FROM Segment WHERE id = %d;
        """ % i['segmentId']) # Q.6
      if len(search) == 0:
        raise NotFound("Segment %d does not exist" % i['segmentId'])
      else:
        match = search[0]
        return {
        'segmentId': match[0],
        'trackLength': match[1],
        'condition': trim(match[2]),
        'startStation': trim(match[3]),
        'endStation': trim(match[4])
      }
    elif 'condition' in i:
      search = self._dbw.execute(
        """
      SELECT * FROM Segment WHERE condition = '%s';
        """ % i['condition']) # Q.7
      results = []
      for s in search:
        sid = s[0]
        results.append(self.get_segment_info({'segmentId': sid}))
      return results
    else:
      raise MissingInput

  def get_segment_status_count(self, i):
    v = self.extract_fields(['status'], i)
    query = None
    if v['status'] is None:
      query = """
      SELECT 
      COUNT(*)
      FROM
          Segment
      WHERE
          condition IS NULL;
      """
    else:
      query = """
      SELECT 
      COUNT(*)
      FROM
          Segment
      WHERE
          condition = '%s';
      """ % v['status'] # Q.10
    result = self._dbw.execute(query)
    return {
      'status': v['status'],
      'numSegments': result[0][0]
    }


  """
  Update Segment status
  """

  def update_segment(self, i):
    v = self.extract_fields(['segmentId'], i)
    seg = self.get_segment_info({ 'segmentId': v['segmentId'] })
    start_station = seg['startStation']
    end_station = seg['endStation']
    length = seg['trackLength']
    status = seg['condition']
    updates = 0
    if 'startStation' in i:
      start_station = i['startStation']
      self.get_station({'sname': start_station})
      updates += 1
    if 'endStation' in i:
      end_station = i['endStation']
      self.get_station({'sname': end_station})
      updates += 1
    if 'length' in i:
      length = i['length']
      updates += 1
      if type(length) is not int:
        raise InputDomainError()
    if 'status' in i:
      status = i['status']
      updates += 1
    if updates == 0:
      raise MissingInput("No fields to update")
    # Q.5
    self._dbw.execute(
      """
      UPDATE Segment 
      SET
        track_length = %d,
        condition = '%s',
        start_station_name = '%s',
        end_station_name = '%s'
      WHERE id = %d;
      """ % (length, status, start_station, end_station, v['segmentId']))
    return {
      'message': 'Segment updated'
    }

  """
  Get overworked workers
  """

  def get_overworked(self):
    query = """
      SELECT W.worker_id 
      FROM Maintenance_Worker W 
      WHERE
      NOT EXISTS 
        (SELECT * 
          FROM Segment S
         WHERE NOT EXISTS
          (SELECT WO.maintenance_worker_id
            FROM Works_On WO
            WHERE W.worker_id = WO.maintenance_worker_id AND 
              S.id = WO.segment_id));
            """ # Q.12
    results = self._dbw.execute(query)
    wids = []
    for r in results:
      wid = r[0]
      wids.append(wid)
    return wids


  """
  Get worker shifts
  """

  def get_worker_shifts(self, i):
    v = self.extract_fields(['workerId'], i)
    wid = v['workerId']
    results = []
    # Q.4
    for r in self._dbw.execute(
      """
      SELECT * from Works_Shift
      WHERE train_worker_id = %d
      """ % wid):
      results.append({
        'tripId': r[1],
        'segmentId': r[2],
        'numHours': r[3],
        'startTime': trim(r[4])
      })
    return results


  """
  Schedule worker shift
  """

  def get_trip_info(self, i):
    v = self.extract_fields(['tripId'], i)
    if type(v['tripId']) is not int:
      raise InputDomainError()
    search = self._dbw.execute(
      """
      SELECT * FROM Trip WHERE id = %d;
      """ % v['tripId']) 
    if len(search) == 0:
      raise NotFound("Trip %d does not exist" % v['tripId'])
    else:
      match = search[0]
      return {
      'departureTime': trim(match[1]),
      'arrivalTime': trim(match[2])
    }

  def schedule_shift(self, i):
    v = self.extract_fields(
      [
        'workerId', 'tripId', 'segmentId', 
        'numHours', 'startTime'
      ], i)
    self.get_segment_info(v)
    self.get_single_worker(v, target_worker_type='Train')
    self.get_trip_info(v)
    search = self._dbw.execute(
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
    self._dbw.execute((
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

  def remove_shift(self, i):
    v = self.extract_fields(
      [
        'workerId', 'tripId', 'segmentId'
      ], i)
    search = self._dbw.execute(
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
    self._dbw.execute(
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

  def get_passenger_info(self, i):
    v = self.extract_fields(['passengerId'], i)
    if type(v['passengerId']) is not int:
      raise InputDomainError()
    search = self._dbw.execute(
      """
      SELECT * FROM Passenger WHERE id = %d;
      """ % v['passengerId'])
    if len(search) == 0:
      raise NotFound("Passenger %d does not exist" % v['passengerId'])
    else:
      match = search[0]
      return {
        'passengerId': v['passengerId'],
        'name': ("%s %s" % (trim(match[1]), trim(match[2]))),
        'phoneNumber': trim(match[3]),
        'email': trim(match[4])
      }

  def get_class_info(self, i):
    v = self.extract_fields(['classType'], i)
    search = self._dbw.execute(
      """
      SELECT * FROM Class WHERE type = '%s';
      """ % v['classType'])
    if len(search) == 0:
      raise NotFound("Class %s does not exist" % v['classType'])
    else:
      match = search[0]
      return {
        'classType': trim(match[0]),
        'refundable': match[1],
        'priorityBoarding': match[2],
        'freeFood': match[3]
      }

  def get_ticket_info(self, i):
    v = self.extract_fields([
      'tripId', 'seatNumber'
    ], i)
    search = self._dbw.execute(
      """
      SELECT * FROM (Ticket
      INNER JOIN
      Passenger
      On
      Passenger.id = Ticket.passenger_id)
      INNER JOIN
      Class
      on
      Class.type = Ticket.class_type
      WHERE 
        Ticket.seat_number = %d
        AND
        Ticket.trip_id = %d
      """ % (v['seatNumber'], v['tripId'])) # Q.9
    if len(search) == 0:
      raise NotFound("Requested ticket does not exist")
    else:
      match = search[0]
      # passenger = self.get_passenger_info({'passengerId': pid})
      # ticketclass = self.get_class_info({'classType': ctype})
      return {
        'seatNumber': match[0],
        'passenger': {
            'passengerId': match[4],
            'name': ("%s %s" % (trim(match[5]), trim(match[6]))),
            'phoneNumber': trim(match[7]),
            'email': trim(match[8])
          },
        'class': {
          'classType': trim(match[2]),
          'refundable': match[11],
          'priorityBoarding': match[12],
          'freeFood': match[13]
        }
      }


  """
  Station stuff
  """

  def create_station(self, i):
    v = self.extract_fields(
      [
        'sname', 'capacity', 'location', 
      ], i)
    if type(v['capacity']) is not int:
      raise InputDomainError("Capacity must be an integer")
    search = self._dbw.execute(
      """
      SELECT * FROM Station
      WHERE 
        name = '%s'
      """ % v['sname'])
    if len(search) > 0:
      raise NotAllowed("Station %s already exists and you cannot add it again" % v['sname'])
    self._dbw.execute((
      """
      INSERT INTO Station VALUES ('%s', '%s', %d);
      """
      % (v['sname'], 
      v['location'], 
      v['capacity'])))
    return {
      'message': "Station created"
    }

  def get_station(self, i):
    if 'sname' in i:
      search = self._dbw.execute(
        """
      SELECT * FROM Station WHERE name = '%s';
        """ % i['sname']) 
      if len(search) == 0:
        raise NotFound("Station %s does not exist" % i['sname'])
      else:
        match = search[0]
        return {
        'sname': trim(match[0]),
        'location': trim(match[1]),
        'trainCapacity': match[2]
      }
    else:
      search = self._dbw.execute(
        """
      SELECT * FROM Station;
        """)
      results = []
      for s in search:
        sname = s[0]
        results.append(self.get_station({'sname': sname}))
      return results

  def update_station(self, i):
    raise HandlerNotImplemented()


  """
  Stats stuff
  """

  def get_avg_trip_length(self):
    query = """
      SELECT AVG (LENGTH.sum_trip_segments) 
      FROM 
        (SELECT SUM(track_length) AS sum_trip_segments
          FROM 
            Trip_Leg 
            INNER JOIN 
            Segment
            ON
            Trip_Leg.segment_id = Segment.id
          GROUP BY trip_id) AS LENGTH
            """ # Q.11
    result = self._dbw.execute(query)
    if result[0][0] is None:
      return {
        'avgTripLength': 0.0
      }
    else:
      return {
        'avgTripLength': float(result[0][0])
      }
