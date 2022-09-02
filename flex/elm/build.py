#! /usr/bin/python
import os
import subprocess
import sys
import hashlib
sys.path.append('../')
from common import *
def build():
    print("Building elm")
    common_func();
    
    