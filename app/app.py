"""
Defines the forward-facing API for the
"Trains 'R' Us" Application
"""


from flask import Flask, request, make_response
import json
from utils import ApplicationLogger
import engine


"""
All of the HTTP status codes we could ever need
"""
SUCCESS_OK = 200
SUCCESS_CREATE = 201
CLIENT_BAD_REQUEST = 400
CLIENT_FORBIDDEN = 403
CLIENT_NOT_FOUND = 405
CLIENT_BAD_METHOD = 405
SERVER_INTERNAL_ERROR = 500
SERVER_NOT_IMPLEMENTED = 501
SERVER_UNAVAILABLE = 503


"""
Request and response helpers that enforce JSON
compliance
"""

def obj_response(o, status_code=SUCCESS_OK):
  """
  Return a response object containing JSON data
  o is the python object (dict) to encode, must
  be JSON friendly
  """
  data = json.dumps(o)
  res = make_response((data, status_code))
  res.headers['Content-Type'] = 'application/json'
  return res


def obj_request(k):
  """
  Attempts to read JSON body from the request context.
  If body is an improper mimetype, returns
  a bad request response. Otherwises passes the
  request to the engine computation k and produces the
  result. Should k result in some error, an appropriate
  response will be sent.
  """
  req = request.get_json()
  if req is None or not isinstance(req,dict):
    return obj_response(
      {
        'message': "You gotta give me a JSON object"
      }, 
      status_code=CLIENT_BAD_REQUEST)
  else:
    logger.info("Request: %s" % json.dumps(req))
    try:
      return k(req)
    except engine.MissingInput as e:
      return obj_response(
      {
        'message': str(e)
      }, 
      status_code=CLIENT_BAD_REQUEST)
    except engine.NotAllowed as e:
      return obj_response(
      {
        'message': str(e)
      }, 
      status_code=CLIENT_FORBIDDEN)
    except Exception as e:
      logger.error("Engine error: %s" % e)
      return obj_response(
      {
        'message': "An internal engine error occurred"
      }, 
      status_code=SERVER_INTERNAL_ERROR)


"""
Set up application context
"""
app = Flask("Trains 'R' Us")
logger = ApplicationLogger()


"""
Routes
"""

VERSION = "v1"

@app.route(('/%s/' % VERSION), methods=["GET"])
def hello():
    return obj_response(engine.sample())
    

@app.route(('/%s/execute' % VERSION), methods=["POST"])
def execute():
    return obj_request(
      lambda r: 
      obj_response(engine.handle_execute(r), status_code=SUCCESS_CREATE))
    

"""
Runtime
"""
if __name__ == "__main__":
    try:
      engine.init_db_wrapper()
      app.run(host="0.0.0.0") # TODO change to env variable
    except Exception as e:
      logger.error("Could not set up database wrapper (see logs)")
