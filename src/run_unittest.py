#!/usr/bin/python
import os
import sys
from unittest import defaultTestLoader as loader, TextTestRunner

suite = loader.discover('./', 'frame_unittest.py')
runner = TextTestRunner()
ret = not runner.run(suite).wasSuccessful()
#sys.exit(ret)
 
