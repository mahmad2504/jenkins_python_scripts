#! /usr/bin/python
import os
import subprocess
import sys
import hashlib
import env

# import all local script

from flex.fir.scripts.generate_oss_tarballs import * 
from flex.parent import *
from common import *

class main(Parent):
    def __init__(self):
        super().__init__()
        print('Script='+os.path.realpath(__file__))
        #################### CONSTANT #################################
        
        self.manifest="fir/mel_update_dev.xml"
        self.base_build_name="mel_fir"
        self.mirrorlocation=self.mirrorlocation+"fir"
        self.syncsourcesto= self.syncsourcesto+"fir"
        
        self.accept_xilinx_eula="true"
        self.systembuilder="/mnt/systembuilder"
        self.buildscripts=self.workspace+"/repotop/scripts"

        ############# Environment Variables #############

        os.environ["base_version"]=self.base_version
        os.environ["buildscripts"]=self.buildscripts
        os.environ['base_build_name']=self.base_build_name
        os.environ['mirrorlocation']=self.mirrorlocation
        os.environ['syncsourcesto']=self.syncsourcesto
        os.environ['sstate_mirror']=self.sstate_mirror
        os.environ['accept_xilinx_eula']=self.accept_xilinx_eula
        os.environ['sbmount']=self.systembuilder
        os.environ['machine']=self.machine
        os.environ['buildtype']='mel'
        os.environ['MGLS_LICENSE_FILE']=self.mgls_license_file
        os.environ['force_shortid']=self.shortid
       

        ###################################################
        # Add any additional path 
        ###################################################
        #self.path=self.path+":/mypath"
        ####################### Default values #################################

    def generate_oss_tarballs(obj):
        generate_oss_tarballs(obj)
        