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
        self.params['BUILD_LOCATION']=os.getenv('BUILD_LOCATION')
              
        if(self.params['WORKSPACE'] == None):
            print('WORKSPACE environment variable is not defined')
            exit(-1)
        if ((self.params['BUILD_NUMBER'] == None) and (self.params['OVERRIDE_BUILD_NUMBER'] == None)):
            print('BUILD_NUMBER environment variable is not defined')
            exit(-1)
        if(self.params['BUILD_LOCATION'] == None):
            print('BUILD_LOCATION environment variable is not defined')
            exit(-1)
        
        
        if(self.params['OVERRIDE_BUILD_NUMBER'] != None):
            self.params['build_folder']=self.params['BUILD_LOCATION']+"/"+self.params['OVERRIDE_BUILD_NUMBER']
        else:
            self.params['build_folder']=self.params['BUILD_LOCATION']+"/"+self.params['BUILD_NUMBER']
        
        printdictionary(self.params,'Parameters')
        if(self.params['OVERRIDE_BUILD_NUMBER'] != None):
            print("Overriding BUILD_NUMBER "+self.params['BUILD_NUMBER']+" with "+self.params['OVERRIDE_BUILD_NUMBER'])
            self.params['BUILD_NUMBER']=self.params['OVERRIDE_BUILD_NUMBER']
        
    def checkout(self):
        checkout(DictObj(self.params))
    