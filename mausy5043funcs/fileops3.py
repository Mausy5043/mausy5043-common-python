#!/usr/bin/env python3

"""
Provides file operation functions.
"""

import os

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
