import sys


class ApplicationLogger:

  def __init__(self, debug_on=True, demo_mode=False):
    self._debug = debug_on
    self._demo = demo_mode

  def _displayln_(self, s):
    sys.stderr.write("%s\n" % s)

  def info(self, msg):
    if not self._demo:
      self._displayln_(" [INFO] %s" % msg)

  def debug(self, msg):
    if self._debug and not self._demo:
      self._displayln_(" [DEBUG] %s" % msg)

  def warn(self, msg):
    if not self._demo:
      self._displayln_(" [WARN] %s" % msg)

  def error(self, msg):
    self._displayln_(" [ERROR] %s" % msg)

  def demo(self, msg):
    if self._demo:
      self._displayln_(" [DEMO] %s" % msg)


def trim_char_seq(s):
    if s is None:
      return None
    elif type(s) is not str:
      raise Exception("Invalid type for char strip: %s" % str(type(s)))
    return s.rstrip(' ')


def loadAuthToken():
    token = None
    try:
        with open("auth.token", "r") as token_file:
            token = token_file.read()
    except Exception:
        raise Exception("Could not load authorization token")
    return token
