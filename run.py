#! /usr/bin/python
import os
import subprocess
import sys

import common
from flex.ginkgo.main import ginkgo as flex_ginkgo
from omni.3_0_x.main import 3_0_x as omni_3_0_x
from tarball.main import tarball

if len(sys.argv)<3:
    print('usage: run <module> <function>')
    exit(-1)
    
module=sys.argv[1].replace(".","_")
funct=sys.argv[2]

try:
    obj = eval(module)()

except Exception as e:
    print(e)
    #print("module "+module.replace("_",".")+" not found")
    exit(-1)

function=None  
try:
    function = getattr(obj,funct)
   

except Exception as e:
    print(e)
    #print(funct+"() not found in "+module+" module")
    exit(-1)

function()


