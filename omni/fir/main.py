#! /usr/bin/python
import os
import subprocess
import sys
import hashlib
import env
from omni.fir.checkout import *
from omni.fir.industrial_pc import *

from common import *
from base import *
class main(Base):
    def __init__(self):
        #################### CONSTANT #################################
        #"ftphost":"sftp://ftpeps.alm.mentorg.com",
        #"ftp_dest_folder":"/pub/mahmad/src/",
        self.params["mel_apt"]=["volt@filesend.embeddedfiles.com:/filesend/volt/omni/common/3.0/apt/base"
                   "volt@filesend.embeddedfiles.com:/filesend/volt/omni/common/3.0/apt/standard"]
        self.params["mel_apt_password"]=env.VOLT_PASSWORD
        #"mel_apt":["narmada@134.86.61.14:omni-3.0-apt/base",
		#          "narmada@134.86.61.14:omni-3.0-apt/standard"]
        self.params["mel_apt_folder"]="/scratch/jenkins/cache/omni3x/mel-apt"
        self.params["pomfile"]="src/cb_unbranched/maven/default_unbranched_settings/pom.xml"
        self.params["jkslocation"]="src/cb_unbranched/resources/signing_cert/release_cert.jks"
        self.params["tsaurl"]="http://timestamp.comodoca.com/authenticode"
        self.params["changelog_duration"]=10
        
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
        self.params['PATH']=":/scratch/jenkins/jdk/bin"
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
    def checkout(self):
        checkout(self)
    def industrial_pc(self):
        industrial_pc(self)
    