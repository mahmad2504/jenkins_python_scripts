#! /usr/bin/python
import os
import subprocess
import sys
import hashlib

from omni.ginkgo.checkout import *
from common import *

class main:
    params={
    "constants":"3.0.0",
    "node":"omni-d10x64-1"

    }
    
    def __init__(self):
    
        self.params['WORKSPACE']=os.getenv('WORKSPACE')
        self.params['BUILD_NUMBER']=os.getenv('BUILD_NUMBER')
        self.params['OVERRIDE_BUILD_NUMBER']=os.getenv('OVERRIDE_BUILD_NUMBER')
        setdefaults()
        printdictionary(self.params,'Parameters')
        self.env=setenvironment(self.params)
    def setdefaults(self):
        print("Defaults")
        if self.params['WORKSPACE']==None:
            self.params['WORKSPACE']='/scratch/jenikns/workspace/temp'
        if self.params['BUILD_NUMBER']==None:
            self.params['BUILD_NUMBER']='build_number'

    def checkout(self):
        print("3.y")
        self.params=DictObj(self.params)
        checkout(self)
        
        
        
    