import requests
import unittest
import time
from utils import TestLogger
import sys

API_MAX_CONNECTION_RETRIES = 10
API_CONNECTION_WAIT = 1

logger = TestLogger()

def test_api(cur_attempts):
    try:
        response = requests.get("http://application:6000/v1/")
        logger.info("Connected!")
        return
    except Exception as e:
      if (cur_attempts + 1) == API_MAX_CONNECTION_RETRIES:
          msg = "No connection to API"
          logger.error(msg)
          sys.exit(1)
      else:
        logger.warn("Trying connection again")
        time.sleep(API_CONNECTION_WAIT)
        return test_api(cur_attempts + 1)

logger.info("Waiting for API to be available...")
test_api(0)

logger.info("Testing Endpoints...")
