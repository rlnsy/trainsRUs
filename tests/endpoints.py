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
  res = method(
    url, 
    data=json.dumps(data) if (data is not None) else None, 
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

  def test_worker_info_2(self):
    res = get(resource("/worker"), data={})
    self.assertEqual(res.status_code, 400)

  def test_worker_info_3(self):
    res = get(resource("/worker"), data={'id': 27837})
    self.assertEqual(res.status_code, 400)

  def test_worker_info_3_pt5(self):
    res = get(resource("/worker"), data={'workerId': "27837"})
    self.assertEqual(res.status_code, 400)

  def test_worker_info_4(self):
    res = get(resource("/worker"), data={'workerId': 27837})
    self.assertEqual(res.status_code, 404)

  def test_worker_info_5(self):
    new_id = post(
      resource("/worker"), 
      data = self.SAMPLE_WORKER, 
      decode_response=True)['data']['workerId']
    res = get(resource("/worker"), data={'workerId': new_id}, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    self.assertEqual(res['data'], self.SAMPLE_WORKER)


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

  NUM_INIT_SEGMENTS = 5

  """ Get segment status """

  def test_segment_status_1(self):
    res = get(resource("/segment"), data={}, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    results = res['data']
    self.assertEqual(len(results), self.NUM_INIT_SEGMENTS)
    self.assertEqual(results[0],
      {
        'segmentId': 1,
        'status': None
      })
    self.assertEqual(results[2],
      {
        'segmentId': 3,
        'status': "Broken"
      })

  def test_segment_status_2(self):
    res = get(resource("/segment"), data={
      'workerId': 6
    }, decode_response=True)
    self.assertEqual(res['response'].status_code, 200)
    results = res['data']
    self.assertEqual(len(results), 1)
    self.assertEqual(results[0],
      {
        'segmentId': 2,
        'status': None
      })


"""
Runtime procedure
"""
if __name__ == '__main__':
  unittest.main()
