#! /usr/bin/python
import os
import subprocess
import sys
import hashlib
sys.path.append('./scripts/flex/ginkgo')
from checkout import *
from common import *
import yaml

class ginkgo:
    params={'repo_url':"ssh://git@github.com:22/MentorEmbedded/mel-manifest.git",'repo_branch':"master"}
    def __init__(self):
        self.params['WORKSPACE']=os.getenv('WORKSPACE')
        self.params['BUILD_NUMBER']=os.getenv('BUILD_NUMBER')
        self.params['OVERRIDE_BUILD_NUMBER']=os.getenv('OVERRIDE_BUILD_NUMBER')
        
        if(self.params['OVERRIDE_BUILD_NUMBER'] != None):
            print("Overriding BUILD_NUMBER "+self.params['BUILD_NUMBER']+" with "+self.params['OVERRIDE_BUILD_NUMBER'])
            self.params['BUILD_NUMBER']=self.params['OVERRIDE_BUILD_NUMBER']
            
        if(self.params['WORKSPACE'] == None):
            print('WORKSPACE environment variable is not defined'
            exit(-1)
        if(self.params['BUILD_NUMBER'] == None):
            print('BUILD_NUMBER environment variable is not defined'
            exit(-1)
    def checkout(self):
        printdictionary(self.params,'Parameters')
        params=DictObj(self.params)
        checkout(params)
    