#! /usr/bin/python
import os
import subprocess
import sys
import hashlib
sys.path.append('./scripts/flex/ginkgo')
from checkout import *
from main_incremental import *
from common import *
import yaml

class ginkgo:
    params={
    'base_version':"13.0.0",
    'repo_url':"ssh://git@github.com:22/MentorEmbedded/mel-manifest.git",
    'repo_branch':"master",
    'default_system_builder':'systembuilder3',
    'base_build_name':"mel_ginkgo_s32g",
    'mirrorlocation':"http://easource.alm.mentorg.com/sources/ginkgo",
    'syncsourcesto':"easource.alm.mentorg.com:/opt/sources/ginkgo",
    'sstate_mirror':"http://easource.alm.mentorg.com/sstate",
    'accept_xilinx_eula':"true",
    'buildscripts':""
    }
    
    def __init__(self):
    
        self.params['WORKSPACE']=os.getenv('WORKSPACE')
        self.params['BUILD_NUMBER']=os.getenv('BUILD_NUMBER')
        self.params['OVERRIDE_BUILD_NUMBER']=os.getenv('OVERRIDE_BUILD_NUMBER')
        self.params['SYSTEM_BUILDER']=os.getenv('SYSTEM_BUILDER')
              
        if(self.params['WORKSPACE'] == None):
            print('WORKSPACE environment variable is not defined')
            exit(-1)
        if ((self.params['BUILD_NUMBER'] == None) and (self.params['OVERRIDE_BUILD_NUMBER'] == None)):
            print('BUILD_NUMBER environment variable is not defined')
            exit(-1)
        if(self.params['SYSTEM_BUILDER'] == None):
            print('SYSTEM_BUILDER environment variable is not defined')
            exit(-1)
        
        if(self.params['SYSTEM_BUILDER'].lower() == 'default'):
            self.params['SYSTEM_BUILDER']=self.params['default_system_builder']
         
        if(self.params['OVERRIDE_BUILD_NUMBER'] != None):
            #print("Overriding BUILD_NUMBER "+self.params['BUILD_NUMBER']+" with "+self.params['OVERRIDE_BUILD_NUMBER'])
            self.params['build_path']="/mnt/"+self.params['SYSTEM_BUILDER']+"/"+self.params['base_build_name']+"/"+self.params['OVERRIDE_BUILD_NUMBER']
        else:
            self.params['build_path']="/mnt/"+self.params['SYSTEM_BUILDER']+"/"+self.params['base_build_name']+"/"+self.params['BUILD_NUMBER']
        
        self.params['buildscripts']=self.params['WORKSPACE']+'/repotop/scripts'
        printdictionary(self.params,'Parameters')
        self.env=setenvironment(self.params)

    def checkout(self):
        self.params=DictObj(self.params)
        checkout(self)
    
    def main_incremental(self):
        self.params=DictObj(self.params)
        main_incremental(self)
    