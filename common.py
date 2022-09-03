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

def sh(command):
    print('>>'+os.getcwd()+'>>'+command)
    result=subprocess.check_output(command, shell=True);
    print(result.decode("utf-8"))
    return result.decode("utf-8")
    
def sh_old(command):
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
       
def checkdiskspace(dspath,dskerrlimit):
    dskspc=int(sh("df -P "+dspath+" | sed '1d' | awk '{print $4}'| tr -d '\n' "))
    if dskspc<=dskerrlimit:
        print("ERROR: Insufficient disk space on "+dspath+" "+dskspc+" KB")
        return -1
    return dskspc