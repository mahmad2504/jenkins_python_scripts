#! /usr/bin/python
import os
import subprocess
import sys

class DictObj:
    def __init__(self, in_dict:dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
               setattr(self, key, [DictObj(x) if isinstance(x, dict) else x for x in val])
            else:
               setattr(self, key, DictObj(val) if isinstance(val, dict) else val)

def checkdiskspace(dspath,dskerrlimit):
	dskspc=os.system("df -P $dspath | sed '1d' | awk '{print $4}' | tr -d '\n'")
	if dskspc<=dskerrlimit:
		printf "ERROR: Insufficient disk space on "+dspath+" "+dskspc KB"
    return dskspc

def sh(command):
    print('>>'+os.getcwd()+'>>'+command)
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Poll process for new output until finished
    while True:
       nextline = process.stdout.readline()
       nextline=nextline.decode("utf-8")
       if nextline == '' and process.poll() is not None:
          break
       sys.stdout.write(nextline)
       sys.stdout.flush()
    output = process.communicate()[0]
    exitCode = process.returncode
    output=output.decode("utf-8")
    if (exitCode == 0):
       if(output != ""):
         print(output)
       return output
    else:
       raise ProcessException(command, exitCode, output)
       