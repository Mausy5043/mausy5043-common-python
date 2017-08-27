"""
Provides file operation functions.
"""

import os
import syslog

def cat(fname):
  """
  Read a file (line-by-line) into a variable.
  Return the variable.
  """
  ret = ""
  if os.path.isfile(fname):
    with open(fname, 'r') as fin:
      ret = fin.read().strip('\n')
  return ret

def lock(fname):
  """
  Create a lockfile
  """
  open(fname, 'a').close()

def unlock(fname):
  """
  Remove a lockfile
  """
  if os.path.isfile(fname):
    os.remove(fname)

def syslog_trace(trace, logerr, out2console):
  """
  Log a (multi-line) message to syslog
  """
  log_lines = trace.split('\n')
  for line in log_lines:
    if line and logerr:
      syslog.syslog(logerr, line)
    if line and out2console:
      print(line)
