#! /usr/bin/python3
import os
import subprocess
import sys
import hashlib
import env
from ml.ver1.build import *
from common import *
from base import *
class main(Base):
    def __init__(self):
        #################### CONSTANT #################################
        
        ############# Environment Variables #############
        self.params['WORKSPACE']=os.getenv('WORKSPACE')
        self.params['BUILD_NUMBER']=os.getenv('BUILD_NUMBER')
        self.params['MANIFEST']=os.getenv('MANIFEST')
        self.params['UPDATE_MEL_APT']=os.getenv('UPDATE_MEL_APT')
        self.params['CHANGE_LOG']=os.getenv('CHANGE_LOG')
        self.params['BUILD_MACHINE']=os.getenv('BUILD_MACHINE')
        ###################################################
        # Add any additional path 
        ###################################################
        ####################### Default values #################################
        if self.params['WORKSPACE']==None:
            self.params['WORKSPACE']='/scratch/jenkins/workspace/scripted_build'
        if self.params['BUILD_NUMBER']==None:
            self.params['BUILD_NUMBER']='build_number'
        if self.params['MANIFEST']==None:
            self.params['MANIFEST']='prod/3.0/omni-3.0.0.xml'  #prod/3.0/all.xml
        if self.params['UPDATE_MEL_APT']==None:
            self.params['UPDATE_MEL_APT']='no'  # yes/no
        if self.params['CHANGE_LOG']==None:
            self.params['CHANGE_LOG']='no'  # yes/no
        if self.params['BUILD_MACHINE']==None:
            self.params['BUILD_MACHINE']="industrial-pc"    
        ########################################################################
        super().__init__(self.params)
    
    ###### Scripts ######
    def build(self):
        build(self)
    