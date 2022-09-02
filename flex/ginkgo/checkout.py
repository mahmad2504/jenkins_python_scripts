#! /usr/bin/python
import os
import subprocess
import sys
import tarfile
import hashlib

from common import *

"""
def uploadtarball()
    mkdir -p /mnt/systembuilder3/mel_ginkgo_s32g/220901_0703
    ${sbmount}/${base_build_name}/${shortid}
"""
 
def checkout():
    print('checkout') 
    """
    os.system('mkdir -p repotop')
    os.chdir('repotop')
    sh('repo init -u ssh://git@github.com:22/MentorEmbedded/mel-manifest.git -b master -m ginkgo/mel_s32g_dev.xml --current-branch')
    sh('repo sync -d -c -q --jobs=10')
    os.chdir('./.repo/manifests')
    sh('git rev-parse HEAD')
    os.chdir('../../../')
    sh('. /mnt/systembuilder/build/scripts/jenkins_preamble checkdiskspace /mnt/systembuilder3  350000000')
    sh('. /mnt/systembuilder/build/scripts/jenkins_preamble checkdiskspace "/var/jenkins" 30000000')
    sh('. /mnt/systembuilder/build/scripts/jenkins_preamble checkkeepfile')
    sh('tar -cjf repotop.tar.bz2 repotop')
    md5=hashlib.md5(open('repotop.tar.bz2','rb').read().hexdigest())
    with open('repotop.txt', 'w') as f:
        f.write(md5)
        f.close()
    """
    
    