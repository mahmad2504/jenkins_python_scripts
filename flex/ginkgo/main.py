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
    def checkout(self):
        params=DictObj(self.params)
        print(yaml.dump(params))
        checkout(DictObj(params));
    
    