#! /usr/bin/python
import os
import subprocess
import sys
import hashlib
sys.path.append('./scripts/omni/3.0.x')
from checkout import *
from main_incremental import *
from common import *

class ginkgo:
    params={
    "constants":"13.0.0"
    }
    
    def __init__(self):
    
        self.params['WORKSPACE']=os.getenv('WORKSPACE')
        self.params['BUILD_NUMBER']=os.getenv('BUILD_NUMBER')
        self.params['OVERRIDE_BUILD_NUMBER']=os.getenv('OVERRIDE_BUILD_NUMBER')
  
        printdictionary(self.params,'Parameters')
        self.env=setenvironment(self.params)

    def checkout(self):
        self.params=DictObj(self.params)
        checkout(self)
    