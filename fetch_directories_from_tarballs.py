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
FOLDERS=os.getenv('FOLDERS') # comma delimited top level folder names 
BUILD_NUMBER=os.getenv('BUILD_NUMBER')
OUTPUT=os.getenv('OUTPUT') 
NODE_NAME=os.getenv('NODE_NAME') 

if AWS_BUCKET==None:
    print('AWS_BUCKET environmental variable not set')
    exit(-1)

if TARBALLS==None:
    print('TARBALLS environmental variable not set')
    exit(-1)
else:
    TARBALLS=TARBALLS.replace("\n", "")

if REBUILD==None:
    REBUILD="no"

if REBUILD=="yes":
    os.system('rm -rf scratch')
    os.system('rm -rf downloads')

if BUILD_NUMBER==None:
    print('BUILD_NUMBER environmental variable not set')
    exit(-1)
else:
    BUILD_NUMBER=str(BUILD_NUMBER)
    
if FOLDERS==None:
    print('FOLDERS environmental variable not set')
    exit(-1)
else:
    FOLDERS=FOLDERS.replace("\n", "")

if OUTPUT==None:
    OUTPUT="output.tar.gz"
  
print("********* Parameters ***********")
print("BUILD_NUMBER=",BUILD_NUMBER)
print("NODE_NAME="+NODE_NAME)
print("AWS_BUCKET="+AWS_BUCKET)
print("REBUILD="+REBUILD)
print("TARBALLS="+TARBALLS)
print("FOLDERS="+FOLDERS)
print("OUTPUT="+OUTPUT)
print("********************************")
TARBALLS=TARBALLS.split(',')
FOLDERS=FOLDERS.split(',')

    
##############################
#Function to pull a file from aws bucket . aws should be configured with appropriate key on the node 
def fetch_aws_file(bucket,filepath,download_folder):
    filename=os.path.basename(filepath)
    if os.path.exists(download_folder+"/"+filename):
        print("Using cached copy of "+filename)
    else:
        print("Downloading "+filename)
        cmd="aws s3 cp s3://"+bucket+filepath+" "+download_folder+"/"
        subprocess.check_output(cmd, shell=True)
    return download_folder+"/"+filename


downloaded_files=[]
os.system('mkdir -p scratch')
os.system('mkdir -p downloads')
try:
    print("Downloading Tarballs from aws")
    for tarball in TARBALLS:
        tarball=tarball.replace("\n", "")
        downloaded_files.append(fetch_aws_file(bucket=AWS_BUCKET,filepath=tarball,download_folder="downloads"))
    os.system('touch scratch/success')
except Exception as e:
    os.system('rm -rf downloads')
    print(e)
    exit(-1)
    
try:
    print("Processing Tarballs")
    for tarball in downloaded_files:
        print("Processing "+tarball)
        if os.path.exists("scratch/success"):
            print("Using cached data ")
        else:
            cmd='tar -xvf '+tarball+' -C scratch'
            subprocess.check_output(cmd, shell=True)
    os.system('touch scratch/success')
except Exception as e:
    os.system('rm -rf scratch')
    print(e)
    exit(-1)

try:
    print("Creating "+OUTPUT+" in "+os.getcwd()+" on node "+NODE_NAME)
    cmd="tar -czf "+OUTPUT
    for folder in FOLDERS:
        folder=folder.replace("\n", "")
        cmd += " scratch/"+folder
    subprocess.check_output(cmd, shell=True)
    print("SUCCESS")
    exit()
except Exception as e:
   print(e)
   exit(-1)
