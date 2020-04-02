import sys


class TestLogger:

  def __init__(self, debug_on=True):
    self._debug = debug_on

  def _displayln_(self, s):
    sys.stderr.write("%s\n" % s)

  def info(self, msg):
    self._displayln_(" [INFO] %s" % msg)

  def debug(self, msg):
    if self._debug:
      self._displayln_(" [DEBUG] %s" % msg)

  def warn(self, msg):
    self._displayln_(" [WARN] %s" % msg)

  def error(self, msg):
    self._displayln_(" [ERROR] %s" % msg)
