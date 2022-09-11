#! /usr/bin/python
import os
import subprocess
import sys
import hashlib

from omni.fir.checkout import *
from omni.fir.industrial_pc import *
from common import *

class main:
    params={
        #"ftphost":"sftp://ftpeps.alm.mentorg.com",
        #"ftp_dest_folder":"/pub/mahmad/src/",
        "mel_apt":["volt@filesend.embeddedfiles.com:/filesend/volt/omni/common/3.0/apt/base",
                   "volt@filesend.embeddedfiles.com:/filesend/volt/omni/common/3.0/apt/standard"],
        #"mel_apt":["narmada@134.86.61.14:omni-3.0-apt/base",
		#          "narmada@134.86.61.14:omni-3.0-apt/standard"]
        "mel_apt_folder":"/scratch/jenkins/cache/omni3x/mel-apt",
        "pomfile":"src/cb_unbranched/maven/default_unbranched_settings/pom.xml",
        "jkslocation":"src/cb_unbranched/resources/signing_cert/release_cert.jks",
        "tsaurl":"http://timestamp.comodoca.com/authenticode" 
        #"http://timestamp.globalsign.com/scripts/timstamp.dll" 
        #http://timestamp.verisign.com/scripts/timstamp.dll

    }
    def __init__(self):
    
        self.params['WORKSPACE']=os.getenv('WORKSPACE')
        self.params['BUILD_NUMBER']=os.getenv('BUILD_NUMBER')
        self.params['MANIFEST']=os.getenv('MANIFEST')
        self.params['UPDATE_MEL_APT']=os.getenv('UPDATE_MEL_APT')

        ###################################################
        # Add any path 
        self.params['PATH']=sh('echo $PATH')
        self.params['PATH']+=":/scratch/jenkins/jdk/bin"
    
        # 
        self.setdefaults()
        printdictionary(self.params,'Parameters')
        
        pwd=sh('pwd').strip()
        if pwd !=self.params['WORKSPACE']:
            print('Current directory does not match with WORKSPACE env variable')
            exit(-1)
        #self.params=DictObj(self.params)

        
    def setdefaults(self):
        print("Defaults")
        if self.params['WORKSPACE']==None:
            self.params['WORKSPACE']='/scratch/jenkins/workspace/scripted_build'
        if self.params['BUILD_NUMBER']==None:
            self.params['BUILD_NUMBER']='build_number'
        if self.params['MANIFEST']==None:
            self.params['MANIFEST']='prod/3.0/omni-3.0.0.xml'  #prod/3.0/all.xml
        if self.params['UPDATE_MEL_APT']==None:
            self.params['UPDATE_MEL_APT']='no'  # no
    def checkout(self):
        print("3.x")
        checkout(self)
    def industrial_pc(self):
        industrial_pc(self)
    