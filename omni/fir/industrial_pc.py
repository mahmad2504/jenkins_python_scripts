#! /usr/bin/python
import os
import subprocess
import sys
import tarfile
import xml.etree.ElementTree as ET

from common import *

def industrial_pc(obj):
    UPDATE_MEL_APT=obj.params['UPDATE_MEL_APT']
    WORKSPACE=obj.params['WORKSPACE']
    mel_apt_folder=obj.params['mel_apt_folder']
    mel_apt=obj.params['mel_apt']
    pomfile=obj.params['pomfile']
    jkslocation=obj.params['jkslocation']
    tsaurl=obj.params['tsaurl']
    #################################################################

    print('Building for industrial PC')
    sh('git lfs install')
    if(UPDATE_MEL_APT=='yes'):
        sh('mkdir -p '+mel_apt_folder)
        os.chdir(mel_apt_folder)
        for apt in mel_apt:
            sh("sshpass -p '5!%AX_Z7' rsync -rvc --delete "+apt+" .")
        os.chdir(WORKSPACE)
    else:
        print('Using cached mel-apt')
    
    os.chdir(mel_apt_folder)
    sh('echo "mel-apt contents:" > "../melapt.list"')
    sh('find -type f >> "../melapt.list"')
    os.chdir(WORKSPACE)

    os.chdir('src')
    sh('rm -rf cb_unbranched')
    sh("git clone ssh://git@stash.alm.mentorg.com:7999/cb/cb_unbranched.git")

   
    os.chdir(WORKSPACE)

    tree = ET.parse(pomfile)
    root=tree.getroot()
    name = 'keystore.alias'
    
    
    sh('rsync -a build9-trusty-cs.sje.mentorg.com:/home/gcc/package-repo/cb_repos/tools/jsign/jsign-3.1.jar .')
    sh('md5sum jsign-3.1.jar')
    sh('java -version;echo $VAR1',env=dict(PATH=obj.params['PATH']))

    ####################################################################################################################
    ps1scripts=sh('find -type f -name *.ps1 -not -path "*/vsix/*" -not -path "*/mel_tools/*" | xargs readlink -f').splitlines()
    keystorealias=root.find("./properties/keystore.alias").text
    keystorepass=root.find("./properties/keystore.password").text

    for ps1script in ps1scripts:
        print(ps1script)
        cmd="java -jar ./jsign-3.1.jar -keystore "+jkslocation+" -alias "+keystorealias+" --storepass "+keystorepass+" --tsaurl "+tsaurl+" "+ps1script
        sh(cmd,env=dict(PATH=obj.params['PATH']))