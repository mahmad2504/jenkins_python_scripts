#! /usr/bin/python
import os
import subprocess
import sys
import tarfile

from common import *

def main_incremental(obj):
    params=obj.params
    env=obj.env
    #print(env)
    cmd='echo $mirrorlocation;tar -xjf '+params.build_path+"/repotop.tar.bz2"
    sh(cmd,env)
    pass