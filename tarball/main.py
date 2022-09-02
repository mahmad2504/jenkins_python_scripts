#! /usr/bin/python
import os
import subprocess
import sys
import hashlib
sys.path.append('./scripts/tarball')
from fetch_directories_from_tarball import *
from tarball_diff import *
from common import *

class tarball:
    def __init__(self):
       pass
    def fetch_directories_from_tarball(self):
        fetch_directories_from_tarball();
    def tarball_diff(self):
        tarball_diff();
        