#! /usr/bin/python
import os
import subprocess
import sys
import tarfile

from common import *

def checkout():
    print('checkout')
    os.system('mkdir -p repotop')
    os.chdir('repotop')
    print(os.getcwd())
    sh('repo init -u ssh://git@github.com:22/MentorEmbedded/mel-manifest.git -b master -m ginkgo/mel_s32g_dev.xml --current-branch')
    sh('repo sync -d -c -q --jobs=10')
    os.chdir('./.repo/manifests')
    print(os.getcwd())
    sh('git rev-parse HEAD')
    os.chdir('../../../')
    print(os.getcwd())
    sh('. /mnt/systembuilder/build/scripts/jenkins_preamble checkdiskspace /mnt/systembuilder3  350000000')
    sh('. /mnt/systembuilder/build/scripts/jenkins_preamble checkdiskspace "/var/jenkins" 30000000')
    sh('. /mnt/systembuilder/build/scripts/jenkins_preamble checkkeepfile')
    sh('tar -cjf repotop.tar.bz2 repotop')
    md5=hashlib.md5(open('repotop.tar.bz2','rb').read().hexdigest())