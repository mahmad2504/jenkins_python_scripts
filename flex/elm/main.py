#! /usr/bin/python
import os
import subprocess
import sys
import hashlib

# import all local script
from flex.fir.checkout import *

# import parent script
from common import *
from base import *
class main(Base):
    def __init__(self):
        #################### CONSTANT #################################
        ############# Environment Variables #############
        self.params['WORKSPACE']=os.getenv('WORKSPACE')
        self.params['BUILD_NUMBER']=os.getenv('BUILD_NUMBER')
        
        ###################################################
        # Add any additional path 
        ###################################################
      
        ####################### Default values #################################
        if self.params['WORKSPACE']==None:
            self.params['WORKSPACE']='/var/jenkins/workspace/scripted_build'
        if self.params['BUILD_NUMBER']==None:
            self.params['BUILD_NUMBER']='build_number'
       
        ########################################################################
        super().__init__(self.params)
    
        pass
    def checkout(self):
        print('checkout')
        pass