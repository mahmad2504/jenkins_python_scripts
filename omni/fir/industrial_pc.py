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
    CHANGE_LOG=obj.params['CHANGE_LOG']
    BUILD_MACHINE=obj.params['BUILD_MACHINE']


    mel_apt_folder=obj.params['mel_apt_folder']
    mel_apt=obj.params['mel_apt']
    pomfile=obj.params['pomfile']
    jkslocation=obj.params['jkslocation']
    tsaurl=obj.params['tsaurl']
    changelog_duration=obj.params['changelog_duration']
    
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


    ##################################################################################################################
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
    print("######### PS1 scripts #########")
    ps1scripts=sh('find -type f -name *.ps1 -not -path "*/vsix/*" -not -path "*/mel_tools/*" | xargs readlink -f').splitlines()
    keystorealias=root.find("./properties/keystore.alias").text
    keystorepass=root.find("./properties/keystore.password").text

    for ps1script in ps1scripts:
        print(ps1script)
        cmd="java -jar ./jsign-3.1.jar -keystore "+jkslocation+" -alias "+keystorealias+" --storepass "+keystorepass+" --tsaurl "+tsaurl+" "+ps1script
        sh(cmd,env=dict(PATH=obj.params['PATH']))

    ######################################################################################################################
    if(CHANGE_LOG=='yes'):
        print("######### Change logs #########")
        svndate=str(getdate(changelog_duration)).split()[0]
        os.chdir("src")
        print("Changes since "+svndate)
        gitdirs=sh('find -name .git | sort | sed -e s,^\./,,').splitlines()
        svndirs=sh('find -name .svn | sort | sed -e s,^\./,,').splitlines()
        print("* git repositories *")
        print(gitdirs)
        pwd=os.getcwd()
        log='Change Logs\n'
        for gitdir in gitdirs:
            log+=removelastchr(gitdir,5)+"\n"
            log+=sh('cd '+gitdir+';git log --reverse --date=short --pretty="%cd  %h  %s" --since="'+str(changelog_duration)+' days ago" || true')
            log+="\n"

        print("* svn repositories *")
        print(svndirs)
        for svndir in svndirs:
            log+=svndir+"\n"
            log+=sh('cd '+svndir+';svn log -r "'+svndate+':HEAD"')
            log+="\n"

        print("* Current source revisions *")
        log+='Current source revisions\n'
        for gitdir in gitdirs:
            rev=sh('cd '+gitdir+';git rev-parse HEAD 2>/dev/null || true').strip()
            print(rev+"  "+removelastchr(gitdir,5))
            log+=rev+"  "+removelastchr(gitdir,5)+"\n"
       
        os.chdir(WORKSPACE)
        with open('changelog.txt', 'w') as f:
            f.write(log)
        
    #####################################################################################
    os.chdir(WORKSPACE);
    os.chdir('src')
    if not os.path.exists('mel-apt'):
        sh('ln -s '+mel_apt_folder)
    else:
        print("mel-apt already exists")
    #####################################################################################
    os.chdir(WORKSPACE)
    sh("sudo ./src/industrial-core/scripts/setup-debian")
    ec1=sh("echo $?").strip()
    print(ec1)

    sh('. ./src/industrial-core/setup-environment -d sokol-omni '+BUILD_MACHINE)
    ec2=sh("echo $?").strip()
    print(ec2)
