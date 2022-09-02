#! /usr/bin/python
import os
import subprocess
import sys

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
       