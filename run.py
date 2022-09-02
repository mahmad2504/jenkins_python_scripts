#! /usr/bin/python
import os
import subprocess
import sys

import common
from flex.ginkgo.main import ginkgo as flex_ginkgo
from tarball.main import tarball

if len(sys.argv)<3:
    print('usage: run <module> <function>')
    exit(-1)
    
module=sys.argv[1].replace(".","_")
funct=sys.argv[2]

try:
    obj = eval(module)()

except (SyntaxError, NameError, TypeError, ZeroDivisionError):
    print("module "+module.replace("_",".")+" not found")
    exit(-1)
    
try:
    function = getattr(obj,funct)
    function()
except AttributeError:
    print(funct+"() not found in "+module+" module")
    exit(-1)

