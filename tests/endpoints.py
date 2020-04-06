import requests
import unittest
import time
from utils import TestLogger
import sys
import json
import copy


"""
API Test Setup procedure
"""

API_MAX_CONNECTION_RETRIES = 10
API_CONNECTION_WAIT = 1
API_VERSION = 'v1'
API = ("http://application:6000/%s" % API_VERSION)


def resource(r):
  return ("%s%s" % (API, r))

logger = TestLogger()

def test_api():
  def poll(cur_attempts):
    try:
        requests.get(resource("/"))
        logger.info("Connected!")
        return
    except Exception:
      if (cur_attempts + 1) == API_MAX_CONNECTION_RETRIES:
          msg = "No connection to API"
          logger.error(msg)
          sys.exit(1)
      else:
        logger.warn("Trying connection again")
        time.sleep(API_CONNECTION_WAIT)
        return poll(cur_attempts + 1)
  poll(0)


"""
Test helpers
"""
def _create_req_(method, url, data, decode_response):
  logger.info("Making request: %s" % json.dumps(data))
  body = json.dumps(data) if (data is not None) else None
  res = None
  if method != requests.get:
    res = method(
      url,
      data=body, 
      headers={'Content-Type':"application/json"})
  else:
    res = method(
      url,
      params={'body': body}, 
      headers={'Content-Type':"application/json"})
  if decode_response:
    try:
      return {
        'response': res,
        'data': json.loads(res.text)
      }
    except json.decoder.JSONDecodeError:
      raise Exception("Unparsable response: %s" % str(res.text))
  else:
    return res
def get(url, data=None, decode_response=False):
  return _create_req_(requests.get, url, data, decode_response)
def post(url, data=None, decode_response=False):
  return _create_req_(requests.post, url, data, decode_response)
def put(url, data=None, decode_response=False):
  return _create_req_(requests.put, url, data, decode_response)
def delete(url, data=None, decode_response=False):
  return _create_req_(requests.delete, url, data, decode_response)


"""
Endpoint Unit Tests
"""

class TestEndpoints(unittest.TestCase):

  def setUp(self):
    logger.info("Waiting for API to be available")
    test_api()
    logger.info("Testing endpoints...")


  """
  Worker endpoints
  """

  SAMPLE_WORKER = {
    "firstName": "John",
    "lastName": "Smith",
    "phoneNumber": "6475234213",
    "role": "Train Conductor",
    "availability": "M T Th F",
    "workerType": "Train" 
  }

  """ Create """

  def test_create_worker_0(self):
    res = post(resource("/worker"))
    self.assertEqual(res.status_code, 400)

  def test_create_worker_2(self):
    res = post(resource("/worker"), data={})
    self.assertEqual(res.status_code, 400)

  def test_create_worker_3(self):
    res = post(resource("/worker"), 
      data={
        'firstName': 'John'
      })
    self.assertEqual(res.status_code, 400)

  def test_create_worker_4(self):
    res1 = post(resource("/worker"),
      data = self.SAMPLE_WORKER, decode_response=True)
    if res1['response'].status_code != 201:
      self.fail(res1['response'].text)
    else:
      self.assertIn('workerId', res1['data'])

  def test_create_worker_5(self):
    create = lambda: post(resource("/worker"),
      data = self.SAMPLE_WORKER, decode_response=True)
    id1 = create()['data']['workerId']
    id2 = create()['data']['workerId']
    self.assertNotEqual(id1, id2)


  """ Remove """

  def test_remove_worker_1(self):
    res = delete(resource("/worker"))
    self.assertEqual(res.status_code, 400)

  def test_remove_worker_2(self):
    res = delete(resource("/worker"), data={})
    self.assertEqual(res.status_code, 400)

  def test_remove_worker_3(self):
    res = delete(resource("/worker"), data={'id': 12345})
    self.assertEqual(res.status_code, 400)

  def test_remove_worker_4(self):
    res = delete(resource("/worker"), data={'workerId': 12345})
    self.assertEqual(res.status_code, 404)

  def test_remove_worker_5(self):
    new_id = post(
      resource("/worker"), 
      data = self.SAMPLE_WORKER, 
      decode_response=True)['data']['workerId']
    res = delete(resource("/worker"), data={'workerId': new_id})
    self.assertEqual(res.status_code, 200)

  def test_remove_worker_6(self):
    new_id = post(
      resource("/worker"), 
      data = self.SAMPLE_WORKER, 
      decode_response=True)['data']['workerId']
    delete(resource("/worker"), data={'workerId': new_id})
    res = delete(resource("/worker"), data={'workerId': new_id})
    self.assertEqual(res.status_code, 404)


  """ Worker info """

  def test_worker_info_1(self):
      res = get(resource("/worker"))
      self.assertEqual(res.status_code, 400)

  def test_worker_info_3_pt5(self):
    res = get(resource("/worker"), data={'workerId': "27837"})
    self.assertEqual(res.status_code, 400)

  def test_worker_info_4(self):
    res = get(resource("/worker"), data={'workerId': 27837})
    self.assertEqual(res.status_code, 404)

  def test_worker_info_12(self):
    new_id = post(
      resource("/worker"), 
      data = self.SAMPLE_WORKER, 
      decode_response=True)['data']['workerId']
    res = get(resource("/worker"), 
      data={
        'workerId': new_id,
      }, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertEqual(res['data']['workerId'], new_id)

  def test_worker_info_5(self):
    new_id = post(
      resource("/worker"), 
      data = self.SAMPLE_WORKER, 
      decode_response=True)['data']['workerId']
    res = get(resource("/worker"), 
      data={
        'workerId': new_id,
        'fields': ['lastName', 'firstName', 'phoneNumber', 'role', 'availability', 'workerType']
      }, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertEqual(res['data'], self.SAMPLE_WORKER)

  def test_worker_info_6(self):
    res = get(resource("/worker"), 
      data={}, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertIs(type(res['data']), list)

  """ test projection """

  def test_worker_info_7(self):
    fields = ['firstName', 'phoneNumber', 'role', 'availability']
    res = get(resource("/worker"), 
      data={
        'fields': fields
      }, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertIs(type(res['data']), list)
    self.assertGreater(len(res['data']), 0)
    for f in fields:
      self.assertIn(f, res['data'][0])
    for f in res['data'][0]:
      self.assertIn(f, fields)

  def test_worker_info_8(self):
    new_id = post(
      resource("/worker"), 
      data = self.SAMPLE_WORKER, 
      decode_response=True)['data']['workerId']
    fields = ['firstName', 'phoneNumber', 'role', 'availability']
    res = get(resource("/worker"), 
      data={
        'workerId': new_id,
        'fields': fields
      }, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    for f in fields:
      self.assertIn(f, res['data'])
    for f in res['data']:
      self.assertIn(f, fields)

  def test_worker_info_9(self):
    fields = ['firstName', 'not a real field', 'role', 'availability']
    res = get(resource("/worker"), 
      data={'fields': fields})
    self.assertEqual(res.status_code, 400)

  def test_worker_info_10(self):
    fields = "cat"
    res = get(resource("/worker"), 
      data={'fields': fields})
    self.assertEqual(res.status_code, 400)

  def test_worker_info_11(self):
    new_id = post(
      resource("/worker"), 
      data = self.SAMPLE_WORKER, 
      decode_response=True)['data']['workerId']
    fields = ['firstName']
    res = get(resource("/worker"), 
      data={
        'workerId': new_id,
        'fields': fields
      }, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    for f in fields:
      self.assertIn(f, res['data'])
    for f in res['data']:
      self.assertIn(f, fields)


  """ Update """

  def test_update_worker_1(self):
    res = put(resource("/worker"), data={'workerId': 1})
    self.assertEqual(res.status_code, 400)

  def test_update_worker_2(self):
    res = put(resource("/worker"), 
      data={
        'workerId': 47378,
        'firstName': 'Adam'
      })
    self.assertEqual(res.status_code, 404)

  def test_update_worker_3(self):
    res = put(resource("/worker"), 
      data={
        'workerId': 1,
        'firstName': 'Adam',
        'favouriteColour': 'blue'
      })
    self.assertEqual(res.status_code, 400)

  def test_update_worker_4(self):
    new_id = post(
      resource("/worker"), 
      data = self.SAMPLE_WORKER, 
      decode_response=True)['data']['workerId']
    new_name = "Adam"
    new_phone = "(123) 456-7890"
    slightly_different_worker = copy.deepcopy(self.SAMPLE_WORKER)
    slightly_different_worker['firstName'] = new_name
    slightly_different_worker['phoneNumber'] = new_phone
    slightly_different_worker['workerId'] = new_id
    res = put(resource("/worker"), 
      data={
        'workerId': new_id,
        'firstName': new_name,
        'phoneNumber': new_phone
      })
    self.assertEqual(res.status_code, 201)
    res2 = get(resource("/worker"), data={'workerId': new_id}, decode_response=True)
    self.assertEqual(res2['response'].status_code, 200)
    updated = res2['data']
    self.assertNotEqual(updated, self.SAMPLE_WORKER)
    self.assertEqual(updated, slightly_different_worker)


  """
  Maintenance worker endpoints
  """

  SAMPLE_SEGMENT = {
    'trackLength': 100,
    'condition': "Looking Good",
    'startStation': "West",
    'endStation': "North"
  }

  NUM_INIT_SEGMENTS = 5

  """ Get segment status """

  def test_segment_status_1(self):
    res = get(resource("/segment/status"), data={}, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    results = res['data']
    self.assertIn({
        'segmentId': 1,
        'trackLength': 100,
        'condition': "Working",
        'startStation': "East",
        'endStation': "West"
      }, results)
    self.assertIn({
        'segmentId': 3,
        'trackLength': 150,
        'condition': "Broken",
        'startStation': "Central",
        'endStation': "West"
      }, results)

  def test_segment_status_2(self):
    res = get(resource("/segment/status"), data={
      'workerId': 6
    }, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    results = res['data']
    self.assertEqual(len(results), 1)
    self.assertEqual(results[0],
      {
        'segmentId': 2,
        'trackLength': 200,
        'condition': None,
        'startStation': "East",
        'endStation': "Central"
      })


  """ Get segment status count """

  def test_segment_status_count_1(self):
    res = get(resource("/segment/status/count"),
      data={})
    self.assertEqual(res.status_code, 400)
    res = get(resource("/segment/status/count"),
      data={'segmentId': 3})
    self.assertEqual(res.status_code, 400)

  def test_segment_status_count_2(self):
    target_status = "Not a valid status"
    res = get(resource("/segment/status/count"),
      data={
        'status': target_status
      }, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertEqual(res['data']['status'], target_status)
    self.assertEqual(res['data']['numSegments'], 0)

  def test_segment_status_count_3(self):
    target_status = None
    res = get(resource("/segment/status/count"),
      data={
        'status': target_status
      }, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertEqual(res['data']['status'], target_status)
    self.assertEqual(res['data']['numSegments'], 3)
  

  """ Add segment """

  def test_add_segment_1(self):
    res = post(resource("/segment"), data={})
    self.assertEqual(res.status_code, 400)
    res = post(resource("/segment"),
      data={
        'trackLength': 3,
        'condition': "Looking Good"
      })
    self.assertEqual(res.status_code, 400)

  def test_add_segment_2(self):
    res = post(resource("/segment"),
      data={
        'trackLengh': "100",
        'condition': "Looking Good",
        'startStation': "West",
        'endStation': "North"
    })
    self.assertEqual(res.status_code, 400)

  def zzzzzz_test_add_segment_3(self):
    res = post(resource("/segment"),
      data=self.SAMPLE_SEGMENT, decode_response=True)
    if res['response'].status_code != 201:
      logger.debug(json.dumps(res['data']))
      self.fail()
    self.assertIn('segmentId', res['data'])


  """ Get segment info """

  def test_segment_info_1(self):
    res = get(resource("/segment"), data={})
    self.assertEqual(res.status_code, 400)

  def test_segment_info_2(self):
    res = get(resource("/segment"), 
      data={
        'segmentId': 690400003
      })
    self.assertEqual(res.status_code, 404)

  def test_segment_info_3(self):
    res = post(resource("/segment"),
      data=self.SAMPLE_SEGMENT, decode_response=True)
    sid = res['data']['segmentId']
    res = get(resource("/segment"), 
      data={
        'segmentId': sid
      }, decode_response=True)
    self.assertEqual(res['data']['segmentId'], sid)
    for k in self.SAMPLE_SEGMENT:
      self.assertEqual(res['data'][k], self.SAMPLE_SEGMENT[k])

  def test_segment_info_4(self):
    res = get(resource("/segment"), 
      data={
        'condition': "Broken"
      }, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertIs(type(res['data']), list)


  """ Update status """

  def test_update_status_1(self):
    res = put(resource("/segment/status"), data={})
    self.assertEqual(res.status_code, 400)
    res = put(resource("/segment/status"),
      data={
        'segmentId': 3
      })
    self.assertEqual(res.status_code, 400)
    res = put(resource("/segment/status"),
      data={
        'newStatus': "Broken"
      })
    self.assertEqual(res.status_code, 400)

  def test_update_status_3(self):
    res = put(resource("/segment/status"),
      data={
        'segmentId': 1,
        'status': "Broken"
      })
    self.assertEqual(res.status_code, 201)
    res = get(resource("/segment"), data={'segmentId': 1}, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertEqual(res['data'],
      {
        'segmentId': 1,
        'condition': "Broken",
        'endStation': "West",
        'startStation': "East",
        'trackLength': 100
      })

  def test_update_status_4(self):
    res = put(resource("/segment/status"),
      data={
        'segmentId': 9999,
        'newStatus': "Broken"
      })
    self.assertEqual(res.status_code, 404)

  def test_update_status_5(self):
    res = put(resource("/segment/status"),
      data={
        'segmentId': 1,
        'length': 3000
      })
    self.assertEqual(res.status_code, 201)
    res = get(resource("/segment"), data={'segmentId': 1}, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertEqual(res['data'],
      {
        'segmentId': 1,
        'condition': "Broken",
        'endStation': "West",
        'startStation': "East",
        'trackLength': 3000
      })

  def test_update_status_5_pt_5(self):
    res = put(resource("/segment/status"),
      data={
        'segmentId': 1,
        'length': "three"
      })
    self.assertEqual(res.status_code, 400)

  def test_update_status_6(self):
    res = put(resource("/segment/status"),
      data={
        'segmentId': 1,
        'endStation': "North",
        'startStation': "West"
      })
    self.assertEqual(res.status_code, 201)
    res = get(resource("/segment"), data={'segmentId': 1}, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertEqual(res['data'],
      {
        'segmentId': 1,
        'condition': "Broken",
        'endStation': "North",
        'startStation': "West",
        'trackLength': 3000
      })

  def test_update_status_7(self):
    res = put(resource("/segment/status"),
      data={
        'endStation': "North",
        'startStation': "West"
      })
    self.assertEqual(res.status_code, 400)

  def test_update_status_8(self):
    res = put(resource("/segment/status"),
      data={
        'segmentId': 1,
        'endStation': "North",
        'startStation': "NOT A REAL STATION"
      })
    self.assertEqual(res.status_code, 404)

  def test_update_status_9(self):
    res = put(resource("/segment/status"),
      data={
        'segmentId': 1,
        'endStation': "NOT A REAL STATION",
        'startStation': "West"
      })
    self.assertEqual(res.status_code, 404)

  
  """
  Overworked worker
  """
  def test_get_overworked_1(self):
    res = post(resource("/worker/overworked"))
    self.assertEqual(res.status_code, 405)

  def test_overworked_2(self):
    res = get(resource("/worker/overworked"), decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertIs(type(res['data']), list)
    self.assertEqual(len(res['data']), 1)
    self.assertEqual(res['data'][0], 9)


  """
  Train worker endpoints
  """

  """ Get shifts """

  def test_get_shifts_1(self):
    res = get(resource("/shift"),
      data={})
    self.assertEqual(res.status_code, 400)
    res = get(resource("/shift"),
      data={'idk': 3})
    self.assertEqual(res.status_code, 400)

  def test_get_shifts_2(self):
    res = get(resource("/shift"),
      data={
        'workerId': 16
      }, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertEqual(len(res['data']), 0)

  def test_get_shifts_3(self):
    res = get(resource("/shift"),
      data={
        'workerId': 10
      }, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertEqual(res['data'][0]['startTime'], '8:00')
    self.assertEqual(res['data'][0]['numHours'], 6)
    self.assertEqual(res['data'][1]['startTime'], '13:00')


  """ Schedule shift """

  def test_create_shift_1(self):
    res = post(resource("/shift"),
      data={})
    self.assertEqual(res.status_code, 400)
    res = post(resource("/shift"),
      data={'workerId': 3})
    self.assertEqual(res.status_code, 400)
    res = post(resource("/shift"),
      data={'workerId': 3, 'segmentId': 4})
    self.assertEqual(res.status_code, 400)

  def test_create_shift_2(self):
    res = post(resource("/shift"),
      data={
        'workerId': 1234567,
        'tripId': 1234567,
        'segmentId': 3215672,
        'numHours': 6,
        'startTime': "10:00"
    })
    self.assertEqual(res.status_code, 404)
    res = post(resource("/shift"),
      data={
        'workerId': 1,
        'tripId': 3215672,
        'segmentId': 2,
        'numHours': 6,
        'startTime': "10:00"
    })
    self.assertEqual(res.status_code, 404)

  def test_create_shift_3(self):
    """
    tests the case where worker id is not for a
    train worker
    """
    res = post(resource("/shift"),
      data={
        'workerId': 1,
        'tripId': 2,
        'segmentId': 3,
        'numHours': 6,
        'startTime': "10:00"
    })
    self.assertEqual(res.status_code, 404)

  def test_create_shift_4(self):
    res = post(resource("/shift"),
      data={
        'workerId': 10,
        'tripId': 2,
        'segmentId': 3,
        'numHours': 6,
        'startTime': "10:00"
    }, decode_response=True)
    self.assertEqual(res['response'].status_code, 201)
    self.assertEqual(res['data']['message'], "Shift created")

  def test_create_shift_5(self):
    res = post(resource("/shift"),
      data={
        'workerId': 10,
        'tripId': 2,
        'segmentId': 3,
        'numHours': 6,
        'startTime': "10:00"
    }, decode_response=True)
    self.assertEqual(res['response'].status_code, 403)
    self.assertIn('message', res['data'])


  """ Drop shift """

  def test_remove_shift_1(self):
    res = delete(resource("/shift"),
      data={})
    self.assertEqual(res.status_code, 400)
    res = delete(resource("/shift"),
      data={'workerId': 3})
    self.assertEqual(res.status_code, 400)
    res = delete(resource("/shift"),
      data={'workerId': 3, 'segmentId': 4})
    self.assertEqual(res.status_code, 400)

  def test_remove_shift_2(self):
    res = delete(resource("/shift"),
      data={
        'workerId': 33039, 
        'segmentId': 39030,
        'tripId': 39303
      })
    self.assertEqual(res.status_code, 404)

  def test_remove_shift_3(self):
    res = delete(resource("/shift"),
      data={
        'workerId': 4,
        'tripId': 1, 
        'segmentId': 2
      })
    self.assertEqual(res.status_code, 404)

  def test_remove_shift_4(self):
    res = delete(resource("/shift"),
      data={
        'workerId': 4,
        'tripId': 1, 
        'segmentId': 1
      })
    self.assertEqual(res.status_code, 200)
    res = delete(resource("/shift"),
      data={
        'workerId': 4,
        'tripId': 1, 
        'segmentId': 1
      })
    self.assertEqual(res.status_code, 404)


  """ Get ticket info """

  def test_ticket_info_1(self):
    res = get(resource("/ticket/info"),
      data={})
    self.assertEqual(res.status_code, 400)
    res = get(resource("/ticket/info"),
      data={'tripId': 3})
    self.assertEqual(res.status_code, 400)

  def test_ticket_info_2(self):
    res = get(resource("/ticket/info"),
      data={
        'tripId': 2, 
        'seatNumber': 3
      })
    self.assertEqual(res.status_code, 404)

  def test_ticket_info_3(self):
    res = get(resource("/ticket/info"),
      data={
        'tripId': 1, 
        'seatNumber': 3
      }, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertEqual(res['data']['seatNumber'], 3)
    self.assertEqual(res['data']['passenger'],
      {
        'passengerId': 1,
        'name': "John Smity",
        'phoneNumber': "(124)-333-3214",
        'email': "uad@gmail.com"
      })
    self.assertEqual(res['data']['class'],
      {
        'classType': 'Business',
        'refundable': True,
        'priorityBoarding': True,
        'freeFood': True
      })


  """
  Statistics endpoints
  """

  def test_get_avg_length_1(self):
    res = post(resource("/stat/trip/length"))
    self.assertEqual(res.status_code, 405)

  def test_get_avg_length_2(self):
    res = get(resource("/stat/trip/length"), decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertEqual(res['data']['avgTripLength'], 1.0)


  """
  Station endpoints
  """

  def test_station_info_1(self):
    res = get(resource("/station"),
      data={
        'sname': "NOT A REAL STATION"
      })
    self.assertEqual(res.status_code, 404)

  def test_station_info_2(self):
    res = get(resource("/station"),
      data={}, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertIs(type(res['data']), list)

  def test_station_info_3(self):
    res = get(resource("/station"),
      data={ 'sname': "East"}, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertEqual(res['data'], 
      {
        'sname': "East",
        'location': "Port City",
        'trainCapacity': 100
      })

  def test_create_station_1(self):
    res = post(resource("/station"),
      data={})
    self.assertEqual(res.status_code, 400)
    res = post(resource("/station"),
      data={'sname': "Hi"})
    self.assertEqual(res.status_code, 400)
    res = post(resource("/station"),
      data={'sname': "HI", 'capacity': 4})
    self.assertEqual(res.status_code, 400)
    res = post(resource("/station"),
      data={'sname': "HI", 'capacity': 4})
    self.assertEqual(res.status_code, 400)
    res = post(resource("/station"),
      data={'sname': "HI", 'location': "Canada", 'capacity': '4'})
    self.assertEqual(res.status_code, 400)

  def test_create_station_2(self):
    res = post(resource("/station"),
      data={
        'sname': "Station Rowan",
        'capacity': 100,
        'location': "Port City"
    }, decode_response=True)
    self.assertEqual(res['response'].status_code, 201)
    self.assertEqual(res['data']['message'], "Station created")

  def test_create_station_3(self):
    res = post(resource("/station"),
      data={
        'sname': "Station Rowan",
        'capacity': 100,
        'location': "Port City"
    }, decode_response=True)
    self.assertEqual(res['response'].status_code, 403)
    self.assertIn('message', res['data'])


"""
Runtime procedure
"""
if __name__ == '__main__':
  unittest.TestLoader.sortTestMethodsUsing = None
  unittest.main()
