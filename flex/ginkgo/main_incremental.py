#! /usr/bin/python
import os
import subprocess
import sys
import tarfile

from common import *

def main_incremental(params):
    cmd='tar -xjf '+params.build_folder+"/repotop.tar.bz2"
    sh(cmd)
    pass