#! /usr/bin/python

import os
import subprocess
import sys

import common
# import all flex classes
from flex.ginkgo.main import main as flex_ginkgo
from flex.elm.main import main as flex_elm
from flex.fir.main import main as flex_fir

# import all omni classes
from omni.fir.main import main as omni_fir

if len(sys.argv)<3:
    print('usage: run <module> <function>')
    exit(-1)
    
module=sys.argv[1].replace(".","_")
funct=sys.argv[2]

try:
    arg=sys.argv[3]
    if(arg=='debug=1'):
        print("Debug mode is ON")
        common.debug=1
except Exception as e:
    print("Debug mode is OFF")
    pass
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


