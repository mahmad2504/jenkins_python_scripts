#!/usr/bin/python3
import os
import subprocess
import sys
import hashlib
from datetime import datetime, timedelta
from termcolor import colored
import shutil
debug=0
def getdate(N):
    return  datetime.now() - timedelta(days=N)

def removelastchr(input_str,count):
    size = len(input_str)
    # Slice string to remove last N characters from string
    out_string = input_str[:size - count]
    return out_string

class DictObj:
    def __init__(self, in_dict:dict):
        assert isinstance(in_dict, dict)
        for key, val in in_dict.items():
            if isinstance(val, (list, tuple)):
               setattr(self, key, [DictObj(x) if isinstance(x, dict) else x for x in val])
            else:
               setattr(self, key, DictObj(val) if isinstance(val, dict) else val)

def sh(command,env=None,showoutput=0):
    cwd=os.getcwd()
    cwd=cwd.replace(os.environ['workspace'], '')
    print(colored('[WS'+cwd+'] ', 'green'),colored(command, 'white'))
    #print('\033[96m'+'['+cwd+'] '+command)
    result=subprocess.check_output(command, shell=True,env=env);
    if(showoutput==1):
        print(colored(result.decode("utf-8"), 'cyan'),colored('', 'white'))
    return result.decode("utf-8")
    
def ash(command):
    cwd=os.getcwd()
    cwd=cwd.replace(os.environ['workspace'], '')
    print(colored('[WS'+cwd+'] ', 'green'),colored(command, 'white'))

    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # Poll process for new output until finished
    while True:
       nextline = process.stdout.readline()
       nextline=nextline.decode("utf-8")
       if nextline == '' and process.poll() is not None:
          break
       print(colored(nextline, 'cyan'),colored('', 'white'))
       #sys.stdout.write(nextline)
       #sys.stdout.flush()
    output = process.communicate()[0]
    exitCode = process.returncode
    output=output.decode("utf-8")
    if (exitCode == 0):
       if(output != ""):
         print(colored(output, 'cyan'),colored('', 'white'))
       return output
    else:
       print(command, exitCode, output)
       exit(-1)
       
def checkdiskspace(dspath,dskerrlimit):
    print('Checking disk space of '+dspath)
    (total, used, free) = shutil.disk_usage(dspath)
    if int(free)<=dskerrlimit:
        print( colored("ERROR: Insufficient disk space on "+dspath+" "+str(free),"red"))
        return -1
    return free
    
def computemd5(filename):
    md5_hash = hashlib.md5()
    with open(filename,"rb") as f:
        # Read and update hash in chunks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            md5_hash.update(byte_block)
    return md5_hash.hexdigest()

def printparams(dct):
    print("**********"+' Environment Variables '+"**********")
    remitems={}
    for item, value in dct.items(): 
        if(item.isupper()):
            print("{}={}".format(item, value))
        else:
            remitems[item]=value
    print("****************"+' Constants '+"*****************")
    for item, value in remitems.items():
        print("{}={}".format(item, value))
    print("********************************************")

def replace_nth(string, old, new, n):
    index_of_occurrence = string.find(old)

    occurrence = int(index_of_occurrence != -1)
    print(occurrence)

    # 👇️ find index of Nth occurrence
    while index_of_occurrence != -1 and occurrence != n:
        index_of_occurrence = string.find(old, index_of_occurrence + 1)
        occurrence += 1

    # 👇️ index of Nth occurrence found, replace substring
    if occurrence == n:
        return (
            string[:index_of_occurrence] + new +
            string[index_of_occurrence+len(old):]
        )