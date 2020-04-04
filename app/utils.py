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
