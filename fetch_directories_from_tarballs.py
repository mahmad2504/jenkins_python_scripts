#! /usr/bin/python
import os
import subprocess
import sys

# input parameter ##########

tarballs_toprocess=[
"/INDLIN/releases/industrial-os-2.4.1/oss/siemens-runtime.tar.gz",
"/INDLIN/releases/industrial-os-2.4.1/oss/ipc-runtime.tar.gz",
"/INDLIN/releases/industrial-os-2.4.1/oss/base-runtime.tar.gz"]
##############################

AWS_BUCKET=os.getenv('AWS_BUCKET') #"filesend.eps.mentorcloudservices.com"
TARBALLS=os.getenv('TARBALLS') #"/INDLIN/releases/industrial-os-2.4.1/oss/siemens-runtime.tar.gz,/INDLIN/releases/industrial-os-2.4.1/oss/ipc-runtime.tar.gz"
REBUILD=os.getenv('REBUILD') # "yes" pr "no"

if AWS_BUCKET==None:
    print('AWS_BUCKET environmental variable not set')

if TARBALLS==None:
    print('TARBALLS environmental variable not set')

if REBUILD==None:
    REBUILD="no"

if REBUILD=="yes":
    os.system('rm -rf scratch')
    os.system('rm -rf downloads')
    
##############################
#Function to pull a file from aws bucket . aws should be configured with appropriate key on the node 
def fetch_aws_file(bucket,filepath,download_folder):
    filename=os.path.basename(filepath)
    if os.path.exists(download_folder+"/"+filename):
        print("Using cached copy of "+filename)
    else:
        print("Donloading "+filename)
        cmd="aws s3 cp s3://"+bucket+filepath+" "+download_folder+"/"
        subprocess.check_output(cmd, shell=True)
    return download_folder+"/"+filename


downloaded_files=[]
os.system('mkdir -p scratch')
try:
  print("Fetching Tarballs from aws")
  for tarball in tarballs_toprocess:
      downloaded_files.append(fetch_aws_file(bucket=AWS_BUCKET,filepath=tarball,download_folder="downloads"))
except Exception as e:
   print(e)

if os.path.exists("scratch"):
   print("Scratch folder exists, remove it and run again")
   exit(-1)
   
try:
  for tarball in downloaded_files:
     print("Processing "+tarball)
     cmd='tar -xvf '+tarball+' -C scratch'
     subprocess.check_output(cmd, shell=True)
except Exception as e:
   print(e)

print("Done")

"/INDLIN/releases/industrial-os-2.4.1/oss/siemens-runtime.tar.gz","/INDLIN/releases/industrial-os-2.4.1/oss/ipc-runtime.tar.gz","/INDLIN/releases/industrial-os-2.4.1/oss/base-runtime.tar.gz"