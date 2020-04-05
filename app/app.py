"""
Defines the forward-facing API for the
"Trains 'R' Us" Application
"""


from flask import Flask, request, make_response
from flask_cors import CORS
import json
from utils import ApplicationLogger
from engine import (
  Engine,
  MissingInput,
  InputDomainError, 
  NotAllowed, 
  NotFound, 
  HandlerNotImplemented
)

"""
All of the HTTP status codes we could ever need
"""
SUCCESS_OK = 200
SUCCESS_CREATE = 201
CLIENT_BAD_REQUEST = 400
CLIENT_FORBIDDEN = 403
CLIENT_NOT_FOUND = 404
CLIENT_BAD_METHOD = 405
SERVER_INTERNAL_ERROR = 500
SERVER_NOT_IMPLEMENTED = 501
SERVER_UNAVAILABLE = 503


"""
Set up application context
"""
app = Flask("Trains 'R' Us")
CORS(app)
logger = ApplicationLogger(demo_mode=True)
engine = Engine(logger)


"""
Request and response helpers that enforce JSON
compliance
"""

def json_response(o, status_code=SUCCESS_OK):
  """
  Return a response object containing JSON data
  o is the python object (dict) to encode, must
  be JSON friendly
  """
  data = json.dumps(o)
  res = make_response((data, status_code))
  res.headers['Content-Type'] = 'application/json'
  return res

def compute_request(k):
  try:
      return k()
  except (
    MissingInput, 
    InputDomainError) as e:
    return json_response(
    {
      'message': str(e)
    }, 
    status_code=CLIENT_BAD_REQUEST)
  except NotAllowed as e:
    return json_response(
    {
      'message': str(e)
    }, 
    status_code=CLIENT_FORBIDDEN)
  except NotFound as e:
    return json_response(
    {
      'message': str(e)
    }, 
    status_code=CLIENT_NOT_FOUND)
  except HandlerNotImplemented as e:
    return json_response(
    {
      'message': str(e)
    }, 
    status_code=SERVER_NOT_IMPLEMENTED)
  except Exception as e:
    logger.error("Engine error: %s" % e)
    return json_response(
    {
      'message': "An internal engine error occurred"
    }, 
    status_code=SERVER_INTERNAL_ERROR)

def obj_request(k):
  """
  Attempts to read JSON body from the request context.
  If body is an improper mimetype, returns
  a bad request response. Otherwises passes the
  request to the engine computation k and produces the
  result. Should k result in some error, an appropriate
  response will be sent.
  """
  req = None
  if request.method == "GET":
    try:
      data = request.args.get('body')
      req = json.loads(data)
    except Exception as e:
      logger.error(str(e))
  else:  
    req = request.get_json()
  if req is None or not isinstance(req,dict):
    return json_response(
      {
        'message': "You gotta give me a JSON object"
      }, 
      status_code=CLIENT_BAD_REQUEST)
  else:
    logger.info("Request: %s" % json.dumps(req))
    return compute_request(lambda: k(req))


"""
Routes
"""

VERSION_1 = "v1"

@app.route(("/%s/" % VERSION_1), methods=["GET"])
def hello():
    return json_response(engine.sample())
    
@app.route(("/%s/execute" % VERSION_1), methods=["POST"])
def execute():
    return obj_request(
      lambda r: 
      json_response(engine.handle_execute(r), status_code=SUCCESS_CREATE))

@app.route(("/%s/worker" % VERSION_1), methods=["POST", "DELETE", "GET", "PUT"])
def worker():
  if request.method == "POST":
    return obj_request(
      lambda r: 
      json_response(engine.create_worker(r), status_code=SUCCESS_CREATE))
  elif request.method == "DELETE":
    return obj_request(
      lambda r: 
      json_response(engine.remove_worker(r), status_code=SUCCESS_OK))
  elif request.method == "GET":
    return obj_request(
      lambda r: 
      json_response(engine.get_single_worker(r), status_code=SUCCESS_OK))
  else:
    return obj_request(
      lambda r: 
      json_response(engine.update_worker(r), status_code=SUCCESS_CREATE))

@app.route(("/%s/segment/status" % VERSION_1), methods=["GET", "PUT"])
def segment_status():
  if request.method == "GET":
    return obj_request(
      lambda r: 
      json_response(engine.get_segments(r), status_code=SUCCESS_OK))
  elif request.method == "PUT":
    return obj_request(
      lambda r: 
      json_response(engine.update_segment(r), status_code=SUCCESS_CREATE))

@app.route(("/%s/segment/status/count" % VERSION_1), methods=["GET"])
def segment_status_count():
  return obj_request(
      lambda r: 
      json_response(engine.get_segment_status_count(r), status_code=SUCCESS_OK))

@app.route(("/%s/segment" % VERSION_1), methods=["GET", "POST"])
def segment():
  if request.method == "GET":
    return obj_request(
      lambda r: 
      json_response(engine.get_segment_info(r), status_code=SUCCESS_OK))
  elif request.method == "POST":
    return obj_request(
      lambda r: 
      json_response(engine.create_segment(r), status_code=SUCCESS_CREATE))
  
@app.route(("/%s/shift" % VERSION_1), methods=["GET", "POST", "DELETE"])
def shiftt():
  if request.method == "GET":
    return obj_request(
      lambda r: 
      json_response(engine.get_worker_shifts(r), status_code=SUCCESS_OK))
  elif request.method == "POST":
    return obj_request(
      lambda r: 
      json_response(engine.schedule_shift(r), status_code=SUCCESS_CREATE))
  elif request.method == "DELETE":
    return obj_request(
      lambda r: 
      json_response(engine.remove_shift(r), status_code=SUCCESS_OK))

@app.route(("/%s/ticket/info" % VERSION_1), methods=["GET"])
def ticket_info():
  return obj_request(
      lambda r: 
      json_response(engine.get_ticket_info(r), status_code=SUCCESS_OK))

@app.route(("/%s/station" % VERSION_1), methods=["GET", "PUT", "POST"])
def station():
  if request.method == "GET":
    return obj_request(
      lambda r: 
      json_response(engine.get_station(r), status_code=SUCCESS_OK))
  elif request.method == "PUT":
    return obj_request(
      lambda r: 
      json_response(engine.update_station(r), status_code=SUCCESS_CREATE))
  elif request.method == "POST":
    return obj_request(
      lambda r: 
      json_response(engine.create_station(r), status_code=SUCCESS_CREATE))

@app.route(("/%s/stat/trip/length" % VERSION_1), methods=["GET"])
def avg_trip_length_stat():
  return compute_request(lambda: json_response(engine.get_avg_trip_length(), status_code=SUCCESS_OK))

@app.route(("/%s/worker/overworked" % VERSION_1), methods=["GET"])
def overworked():
  return compute_request(lambda: json_response(engine.get_overworked(), status_code=SUCCESS_OK))
      

"""
Runtime
"""
if __name__ == "__main__":
    try:
      app.run(host="0.0.0.0", port=6000) # TODO change to env variable
    except Exception as e:
      logger.error("Could not set up database wrapper (see logs)")
