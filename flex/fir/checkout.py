#! /usr/bin/python
import os
import subprocess
import sys
import tarfile
import hashlib
import shutil

from common import *

def checkout2(obj):
    repo_url=obj.repo_url
    repo_branch=obj.repo_branch
    manifest=obj.manifest
    os.system('mkdir -p repotop')
    os.chdir('repotop')
    sh('repo init -u '+repo_url+' -b '+repo_branch+' -m '+manifest+' --current-branch')
    sh('repo sync -d -c -q --jobs=10')
    sh('repo manifest -o - -r')
    os.chdir('./.repo/manifests')
    sh('git rev-parse HEAD',showoutput=1)
    

def configure2(obj):
    sbmount=obj.params['systembuilder']
    base_build_name=obj.params['base_build_name']
    shortid=obj.params['SHORTID']
    machine=obj.params['MACHINE']
    workspace=obj.params['WORKSPACE']
    with open(r'repotop/scripts/jenkins_mel', 'r') as file:
        data = file.read()
        data=replace_nth(data, "install_tools", "", 2)
        data = data.replace('add_image_features "${build_image_features}"', 'exit 0\n')
        with open(r'jenkins_mel', 'w') as file:
            file.write(data)
    sh('chmod a+x jenkins_mel')
    sh_old('./jenkins_mel')

    with open(r'build_'+machine+"/conf/local.conf", 'r') as file:
         data = file.read()
         #print(data)
         data += 'INHERIT += "archiver"\n'
         data += 'BB_GIT_SHALLOW = "0"\n'
         data += 'ARCHIVER_MODE[src] = "original"\n'
         data += 'TOOLCHAINS_PATH = "'+workspace+'/toolchain/toolchains"'
         with open(r'build_'+machine+"/conf/local.conf", 'w') as file:
            file.write(data)
            file.close()

def build2(obj):
    sbmount=obj.params['systembuilder']
    base_build_name=obj.params['base_build_name']
    shortid=obj.params['SHORTID']
    machine=obj.params['MACHINE']
    
    difffile="ossdiff_"+machine+"_mel.txt"
    sh('cp '+sbmount+"/"+base_build_name+"/"+shortid+"/"+difffile+" .")
    packages={}
    with open(difffile, 'r') as file:
        lines = file.readlines()
        for line in lines:
            package_name=line.split(",")[0]
            packages[package_name]=package_name
            
    for key in packages:
        package=packages[key]
        os.chdir('build_'+machine)
        print("bitbake -c ar_original "+package+";bitbake -f -c deploy_archives "+package)
        sh_old("bitbake -c ar_original "+package+";bitbake -f -c deploy_archives "+package)
     
    
def artifacts(obj):
    machine=obj.params['MACHINE']
    shortid=obj.params['SHORTID']
    sbmount=obj.params['systembuilder']
    base_build_name=obj.params['base_build_name']
    
    source_directory='build_'+machine+"/tmp/deploy/sources"
    archive_name="sources_"+machine+".tar.gz"
    cmd='tar -zcvf '+archive_name+' '+source_directory
    sh(cmd)
    
    sh('cp '+archive_name+" "+sbmount+"/"+base_build_name+"/"+shortid+"/"+archive_name,showoutput=1)

def untar(obj):
    WORKSPACE=obj.params['WORKSPACE']
    preamble=obj.params['preamble']
    sh(preamble+" untar",showoutput=1)
