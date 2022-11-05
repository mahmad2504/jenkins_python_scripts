#! /usr/bin/python
import os
import subprocess
import sys
import hashlib
import env

# import all local script

from flex.fir.checkout import *
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
       
        #export MACHINE=imx6ullevk-mel
        #export shortid=220930_1138
        #export force_shortid=220930_1138
        #export BASE_VERSION=12.0.5
        #export WORKSPACE=/var/jenkins/mahmad/workspace
        ########################################################################

    ############################################################################
    #machine=imx6qsabresd-mel
    #machine=imx6ullevk-mel
    #shortid=220823_1053
    #base_version=12.0.5
    #WORKSPACE=/var/jenkins/mahmad/workspace
    #############################################################################
    def generate_oss_tarballs(obj):
        count=0
        try:
            build_folder=obj.systembuilder+"/"+obj.base_build_name+"/"+obj.shortid
            files=os.listdir(build_folder)
            for file in files:
                if "ossdiff" in file:
                    count=count+1
        except:
            print('folder '+build_folder+' does not exist')
            exit(-1)
        if(count==0):
            print('no ossdiff files found in '+build_folder)
            exit(-1)
        Parent.fetch_and_untar_repotop(obj)
        Parent.install_toolchain(obj)
        Parent.configure(obj)
        Parent.fetch_sources(obj)
        Parent.upload_sources(obj)
   