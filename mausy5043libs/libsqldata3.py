import os
import subprocess
import sys
import time
import mausy5043funcs.fileops3 as mf
from random import randrange as rnd

DEBUG = False
# leaf = os.path.realpath(__file__).split('/')[-2]

class SqlDataFetch(object):
  """
  SqlDataFetch:
  Manages retrieval of data from the MySQL server

  Takes these initialisation parameters:
    query_path  absolute path to where the SQL query scripts can be found.
                eg.: "/home/pi/lnxdiagd/queries"
    semaphore_path  absolute path to where the semaphore is handled
                    This directory should contain a "bin" folder with at least
                    the following scripts:
                    - claim
                    - release
                    - check
                    This directory should also contain a "sql" folder where the
                    semaphore file "stack" is kept
                    eg.: "/srv/semaphores"
    h_time      number of *minutes* between successive calls to the hour.sh script
    d_time      number of *minutes* between successive calls to the day.sh script
    w_time      number of *hours* between successive calls to the week.sh script
    y_time      number of *hours* between successive calls to the year.sh script
  """
  def __init__(self, query_path, semaphore_path, h_time, d_time, w_time, y_time):
    super(SqlDataFetch, self).__init__()
    if query_path.endswith('/'):
      query_path = query_path[:-1]
    if semaphore_path.endswith('/'):
      semaphore_path = semaphore_path[:-1]
    self.home           = os.environ['HOME']
    self.version        = 3.0
    self.h_ptr          = 0
    self.d_ptr          = 1
    self.w_ptr          = 2
    self.y_ptr          = 3
    self.claimcmd       = semaphore_path + '/bin/claim'
    self.checkcmd       = semaphore_path + '/bin/check'
    self.releasecmd     = semaphore_path + '/bin/release'
    self.cmd[self.h_ptr]          = query_path + '/hour.sh'
    self.updatetime[self.h_ptr]   = h_time * 60
    self.timer[self.h_ptr]        = time.time() + rnd(60, self.updatetime[self.h_ptr])
    self.cmd[self.d_ptr]          = query_path + '/day.sh'
    self.updatetime[self.d_ptr]   = d_time * 60
    self.timer[self.d_ptr]        = time.time() + rnd(60, self.updatetime[self.d_ptr])
    self.cmd[self.w_ptr]          = query_path + '/week.sh'
    self.updatetime[self.w_ptr]   = w_time * 3600
    self.timer[self.w_ptr]        = time.time() + rnd(60, self.updatetime[self.w_ptr])
    self.cmd[self.y_ptr]          = query_path + '/year.sh'
    self.updatetime[self.y_ptr]   = y_time * 3600
    self.timer[self.y_ptr]        = time.time() + rnd(60, self.updatetime[self.y_ptr])

  def get(self, ptr):
    """
    Get the requested data now.
    """
    mf.syslog_trace("...:  {0}".format(self.cmd[ptr]), False, DEBUG)
    subprocess.call(self.cmd[ptr])

  def fetch(self):
    """
    Manage staleness of the data and get it when needed.
    Play nice; use the CLAIM-CHECK-ACT-RELEASE mechanism
    """
    self.claim_server()

    while True:
      ack = self.check_server()
      mf.syslog_trace("...:  {0}".format(ack), False, DEBUG)
      if (ack <= 1):
        break
      time.sleep(3)

    if (ack == 1):  # ack can also be 0. In that case we've dropped off the stack and need to re-claim.
      t0 = time.time()
      for ptr in range(4):
        if t0 >= self.timer[ptr]:
          self.get(ptr)
          self.timer[ptr] = t0 + self.updatetime[ptr] + rnd(-60, 60)

    self.release_server()
    # ack can be <1 (unsuccesful) or 1 (successful)
    return ack

  def claim_server(self):
    mf.syslog_trace("...:  CLAIM", False, DEBUG)
    return subprocess.call(self.claimcmd)

  def check_server(self):
    mf.syslog_trace("...:  CHECK", False, DEBUG)
    return subprocess.call(self.checkcmd)

  def release_server(self):
    mf.syslog_trace("...:  RELEASE", False, DEBUG)
    return subprocess.call(self.releasecmd)


if __name__ == '__main__':

  DEBUG = True

  print("**** Initialisation ****")
  sqldata = SqlDataFetch("/tmp", "/srv", 1, 1, 1, 1)
  if (sqldata.version != 3.0):
    sys.exit("WRONG VERSION")
  print("OK")
