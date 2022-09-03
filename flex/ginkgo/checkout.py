#! /usr/bin/python
import os
import subprocess
import sys
import tarfile
import hashlib
import shutil

from common import *

def uploadtarball(params):
    cmd='mkdir -p '+params.build_folder
    sh(cmd)
    cmd='cp repotop.tar.bz2 repotop.txt '+params.build_folder+"/"
    sh(cmd)

def checkout(params):
    os.system('mkdir -p repotop')
    os.chdir('repotop')
    sh('repo init -u '+params.repo_url+' -b '+params.repo_branch+' -m '+'ginkgo/mel_s32g_dev.xml'+' --current-branch')
    sh('repo sync -d -c -q --jobs=10')
    os.chdir('./.repo/manifests')
    sh('git rev-parse HEAD')
    os.chdir('../../../')
    
    retval=checkdiskspace('/mnt/systembuilder3',350000000)
    if(retval == -1):
        exit(-1)
    
    retval=checkdiskspace(params.WORKSPACE,30000000)
    if(retval == -1):
        exit(-1)
   
    sh('tar -cjf repotop.tar.bz2 repotop')
    md5=computemd5('repotop.tar.bz2')
    print("md5 checksum is "+md5)
    with open('repotop.txt', 'w') as f:
        f.write(md5)
        f.close()
    
    uploadtarball(params)
    """
    md5=hashlib.md5(open('repotop.tar.bz2','rb').read().hexdigest())
    with open('repotop.txt', 'w') as f:
        f.write(md5)
        f.close()
    """
    
        


    
    