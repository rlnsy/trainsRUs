import requests
import unittest
import time
from utils import TestLogger
import sys
import json


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
  res = method(
    url, 
    data=json.dumps(data) if data else None, 
    headers={'Content-Type':"application/json"})
  if decode_response:
    return {
      'response': res,
      'data': json.loads(res.text)
    }
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

  def test_create_worker_1(self):
    res = get(resource("/worker"), data={})
    self.assertEqual(res.status_code, 405)

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


"""
Runtime procedure
"""
if __name__ == '__main__':
  unittest.main()
