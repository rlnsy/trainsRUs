import sys


class ApplicationLogger:

  def _displayln_(self, s):
    sys.stderr.write("%s\n" % s)

  def info(self, msg):
    self._displayln_(" [INFO] %s" % msg)

  def error(self, msg):
    self._displayln_(" [ERROR] %s" % msg)
