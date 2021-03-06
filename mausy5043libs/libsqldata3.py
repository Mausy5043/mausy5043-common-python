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
  def __init__(self, query_path, semaphore_path, h_time, d_time, w_time, y_time, dbg=False):
    super(SqlDataFetch, self).__init__()
    self.DEBUG          = dbg
    if query_path.endswith('/'):
      query_path        = query_path[:-1]
    if semaphore_path.endswith('/'):
      semaphore_path    = semaphore_path[:-1]
    self.home           = os.environ['HOME']
    self.version        = 3.0
    self.h_ptr          = 0
    self.d_ptr          = 1
    self.w_ptr          = 2
    self.y_ptr          = 3
    self.claimcmd       = semaphore_path + '/bin/claim'
    self.checkcmd       = semaphore_path + '/bin/check'
    self.releasecmd     = semaphore_path + '/bin/release'
    self.querycmd       = [query_path + '/hour.sh', query_path + '/day.sh', query_path + '/week.sh', query_path + '/year.sh']
    self.updatetime     = [h_time * 60, d_time * 60, w_time * 3600, y_time * 3600]
    self.timer          = [time.time(),
                           time.time(),
                           time.time(),
                           time.time()]

  def __get(self, ptr):
    """
    Get the requested data now.
    """
    mf.syslog_trace("...:  {0}".format(self.querycmd[ptr]), False, self.DEBUG)
    subprocess.call(self.querycmd[ptr])

  def fetch(self):
    """
    Manage staleness of the data and get it when needed.
    Play nice; use the CLAIM-CHECK-ACT-RELEASE mechanism
    """
    self.claim_server()

    while True:
      ack = self.check_server()
      mf.syslog_trace("...:  {0}".format(ack), False, self.DEBUG)
      if (ack <= 1):
        break
      time.sleep(3)

    if (ack == 1):  # ack can also be 0. In that case we've dropped off the stack and need to re-claim.
      t0 = time.time()
      for ptr in range(4):
        if t0 >= self.timer[ptr]:
          self.__get(ptr)
          self.timer[ptr] = t0 + self.updatetime[ptr] + rnd(-60, 60)

    self.release_server()
    # ack can be <1 (unsuccesful) or 1 (successful)
    return ack

  def claim_server(self):
    """
    Call the CLAIM command
    """
    mf.syslog_trace("...       :  CLAIM", False, self.DEBUG)
    return subprocess.call(self.claimcmd)

  def check_server(self):
    """
    Call the CHECK command
    """
    mf.syslog_trace("...       :  CHECK", False, self.DEBUG)
    return subprocess.call(self.checkcmd)

  def release_server(self):
    """
    Call the RELEASE command
    """
    mf.syslog_trace("...       :  RELEASE", False, self.DEBUG)
    return subprocess.call(self.releasecmd)


if __name__ == '__main__':

  DEBUG = True

  print("**** Initialisation ****")
  sqldata = SqlDataFetch("/tmp", "/srv", 1, 1, 1, 1, DEBUG)
  if (sqldata.version != 3.0):
    sys.exit("WRONG VERSION")
  print("OK")
