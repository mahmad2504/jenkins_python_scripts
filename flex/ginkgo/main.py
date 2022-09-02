#! /usr/bin/python
import os
import subprocess
import sys
import hashlib
sys.path.append('./scripts/flex/ginkgo')
from checkout import *
from common import *

class ginkgo:
    def __init__(self):
        self.WORKSPACE=os.getenv('WORKSPACE')
        self.BUILD_NUMBER=os.getenv('BUILD_NUMBER')
        pass
    def checkout(self):
        checkout();
    
    