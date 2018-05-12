import os
import subprocess
import sys
import time
import mausy5043funcs.fileops3 as mf
from random import randrange as rnd

DEBUG = False
# leaf = os.path.realpath(__file__).split('/')[-2]

class Graph(object):
  """
  class Graph:
  Executes the <script> to create trendgraphs

  Takes these initialisation parameters:
    script      absolute path to where the graphing script can be found
                eg.: "/home/pi/lnxdiagd/mkgraphs.sh"
    updatetime  number of minutes between successive calls to the script
  """
  def __init__(self, script, updatetime, dbg=False):
    super(Graph, self).__init__()
    self.DEBUG      = dbg
    self.home       = os.environ['HOME']
    self.version    = 3.0
    self.updatetime = updatetime * 60
    self.timer      = time.time()
    self.command    = script

  def __draw(self):
    """
    Draw the graphs.
    Now!
    """
    mf.syslog_trace("...drawing :  {0}".format(self.command), False, self.DEBUG)
    return subprocess.call(self.command)

  def make(self):
    """
    Manage staleness of graphs and draw them when needed.
    """
    t0 = time.time()
    result = 1
    if t0 >= self.timer:
      result = self.__draw()
      t1 = time.time()
      self.timer = t1 + self.updatetime + rnd(-60, 60)
    return result


if __name__ == '__main__':

  DEBUG = True

  print("**** Initialisation ****")
  trendgraph = Graph("/tmp/script", 3, DEBUG)
  if (trendgraph.version != 3.0):
    sys.exit("WRONG VERSION")
