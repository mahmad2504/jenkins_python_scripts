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
BUILD_NUMBER =os.getenv('BUILD_NUMBER ')  
OUTPUT=os.getenv('OUTPUT') 

if AWS_BUCKET==None:
    print('AWS_BUCKET environmental variable not set')
    exit(-1)

if TARBALLS==None:
    print('TARBALLS environmental variable not set')
    exit(-1)

if REBUILD==None:
    REBUILD="no"

if REBUILD=="yes":
    os.system('rm -rf scratch')
    os.system('rm -rf downloads')

if FOLDERS==None:
    print('FOLDERS environmental variable not set')
    exit(-1)


if OUTPUT==None:
    OUTPUT="output.tar.gz"
  
print("********* Parameters ***********")
print("BUILD_NUMBER ="+BUILD_NUMBER)
print("AWS_BUCKET="+AWS_BUCKET)
print("REBUILD="+REBUILD)
print("TARBALLS="+TARBALLS)
print("FOLDERS"+FOLDERS)
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
    for tarball in tarballs_toprocess:
        downloaded_files.append(fetch_aws_file(bucket=AWS_BUCKET,filepath=tarball,download_folder="downloads"))
except Exception as e:
    os.system('rm -rf downloads')
    print(e)
    exit(-1)
    
try:
    print("Processing Tarballs")
    for tarball in downloaded_files:
        print("Processing "+tarball)
        if os.path.exists(scratch):
            print("Using cached data ")
        else:
            cmd='tar -xvf '+tarball+' -C scratch'
            subprocess.check_output(cmd, shell=True)
except Exception as e:
    os.system('rm -rf scratch')
    print(e)
    exit(-1)

try:
    cmd="tar -czf "+BUILD_NUMBER+OUTPUT
    for folder in FOLDERS:
        cmd += " scratch/"+folder
    subprocess.check_output(cmd, shell=True)
    print("Done")
    exit()
except Exception as e:
   print(e)
   exit(-1)