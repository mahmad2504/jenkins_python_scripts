#! /usr/bin/python
import os
import subprocess
import sys
import tarfile
import hashlib
import shutil

from common import *

def checkout(obj):
    MANIFEST=obj.params['MANIFEST']
    WORKSPACE=obj.params['WORKSPACE']
    ################################################################
    #ftphost=obj.params.ftphost
    #ftp_dest_folder=obj.params.ftp_dest_folder
    sh('mkdir -p src')
    os.chdir('src')
    sh('pwd')
    sh('repo init -u git@github.com:MentorEmbedded/industrial-manifest -m '+MANIFEST)
    sh('repo sync')
    os.chdir(WORKSPACE)
    #sh('tar -cjf src.tar.bz2 src/')
    #sh('lftp -e "cd '+ftp_dest_folder+'; rm -f src.tar.bz2; put src.tar.bz2; bye" '+ftphost)

   
    
    
    