#!/usr/bin/env python3

# testd.py is used to test libdaemon3

import os
import sys
import syslog
import time
import traceback

from mausy5043libs.libdaemon3 import Daemon

# constants
DEBUG       = False
IS_JOURNALD = os.path.isfile('/bin/journalctl')
MYAPP       = os.path.realpath(__file__).split('/')[-2]
NODE        = os.uname()[1]

# initialise logging
syslog.openlog(ident=MYAPP, facility=syslog.LOG_LOCAL0)

class MyDaemon(Daemon):
  """Definition of daemon"""
  @staticmethod
  def run():
    """Execute a simple cycle to simulate a daemonprocess"""
    reporttime      = 60
    samplespercycle = 3
    sampletime      = reporttime/samplespercycle    # time [s] between samples
    syslog_trace("DEBUG       : {0}".format(DEBUG), syslog.LOG_DEBUG, DEBUG)
    syslog_trace("IS_JOURNALD : {0}".format(IS_JOURNALD), syslog.LOG_DEBUG, DEBUG)
    syslog_trace("MYAPP       : {0}".format(MYAPP), syslog.LOG_DEBUG, DEBUG)
    syslog_trace("NODE        : {0}".format(NODE), syslog.LOG_DEBUG, DEBUG)

    while True:
      try:
        starttime   = time.time()
        result      = starttime
        syslog_trace("Result   : {0}".format(result), False, DEBUG)

        waittime    = sampletime - (time.time() - starttime) - (starttime % sampletime)
        if (waittime > 0):
          syslog_trace("Waiting  : {0}s".format(waittime), False, DEBUG)
          syslog_trace("................................", False, DEBUG)
          syslog_trace("..still alive..", syslog.LOG_DEBUG, False)
          time.sleep(waittime)
      except Exception:
        syslog_trace("Unexpected error in run()", syslog.LOG_CRIT, DEBUG)
        syslog_trace(traceback.format_exc(), syslog.LOG_CRIT, DEBUG)
        raise

def syslog_trace(trace, logerr, out2console):
  """Log a python stack trace to syslog"""
  log_lines = trace.split('\n')
  for line in log_lines:
    if line and logerr:
      syslog.syslog(logerr, line)
    if line and out2console:
      print(line)


if __name__ == "__main__":
  daemon = MyDaemon('/tmp/test.pid')
  if (daemon.version != 3):
    sys.exit("WRONG VERSION")
  if len(sys.argv) == 2:
    if 'start' == sys.argv[1]:
      daemon.start()
    elif 'stop' == sys.argv[1]:
      daemon.stop()
    elif 'restart' == sys.argv[1]:
      daemon.restart()
    elif 'test' == sys.argv[1]:
      # assist with debugging.
      print("Debug-mode started. Use <Ctrl>+C to stop.")
      DEBUG = True
      syslog_trace("Daemon logging is ON", syslog.LOG_DEBUG, DEBUG)
      daemon.run()
    else:
      print("Unknown command")
      sys.exit(2)
    sys.exit(0)
  else:
    print("usage: {0!s} start|stop|restart|test".format(sys.argv[0]))
    sys.exit(2)
