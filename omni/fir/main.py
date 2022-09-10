#! /usr/bin/python
import os
import subprocess
import sys
import hashlib

from omni.fir.checkout import *
from common import *

class main:
    params={
    "constants":"3.0.0"
    }
    
    def __init__(self):
    
        self.params['WORKSPACE']=os.getenv('WORKSPACE')
        self.params['BUILD_NUMBER']=os.getenv('BUILD_NUMBER')
        self.params['OVERRIDE_BUILD_NUMBER']=os.getenv('OVERRIDE_BUILD_NUMBER')
  
        printdictionary(self.params,'Parameters')
        self.env=setenvironment(self.params)

    def checkout(self):
        print("3.x")
        self.params=DictObj(self.params)
        checkout(self)
    