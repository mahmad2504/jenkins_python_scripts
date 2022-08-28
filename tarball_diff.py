#! /usr/bin/python
import os
import subprocess
import sys
import tarfile

# input parameter ##########

AWS_BUCKET=os.getenv('AWS_BUCKET') #"filesend.eps.mentorcloudservices.com"
TARBALLSv1=os.getenv('TARBALLSv1') #"/INDLIN/releases/industrial-os-2.4.1/oss/siemens-runtime.tar.gz,/INDLIN/releases/industrial-os-2.4.1/oss/ipc-runtime.tar.gz"
TARBALLSv2=os.getenv('TARBALLSv2') #"/INDLIN/releases/industrial-os-2.4.1/oss/siemens-runtime.tar.gz,/INDLIN/releases/industrial-os-2.4.1/oss/ipc-runtime.tar.gz"
REBUILD=os.getenv('REBUILD') # "yes" pr "no"
BUILD_NUMBER=os.getenv('BUILD_NUMBER')
NODE_NAME=os.getenv('NODE_NAME') 

if AWS_BUCKET==None:
    print('AWS_BUCKET environmental variable not set')
    exit(-1)

if TARBALLSv1==None:
    print('TARBALLSv1 environmental variable not set')
    exit(-1)
else:
    TARBALLSv1=TARBALLSv1.replace("\n", "")
    
if TARBALLSv2==None:
    print('TARBALLSv2 environmental variable not set')
    exit(-1)
else:
    TARBALLSv2=TARBALLSv2.replace("\n", "")

if REBUILD==None:
    REBUILD="no"

if REBUILD=="yes":
    os.system('rm -rf downloads')

  
print("********* Parameters ***********")
print("BUILD_NUMBER=",BUILD_NUMBER)
print("NODE_NAME="+NODE_NAME)
print("AWS_BUCKET="+AWS_BUCKET)
print("REBUILD="+REBUILD)
print("TARBALLSv1="+TARBALLSv1)
print("TARBALLSv2="+TARBALLSv2)

print("********************************")
TARBALLSv1=TARBALLSv1.split(',')
TARBALLSv2=TARBALLSv2.split(',')
    
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


downloaded_filesv1=[]
os.system('mkdir -p downloadsv1')
os.system('mkdir -p downloadsv2')

try:
    print("Downloading V1 Tarballs from aws")
    for tarball in TARBALLSv1:
        tarball=tarball.replace("\n", "")
        downloaded_filesv1.append(fetch_aws_file(bucket=AWS_BUCKET,filepath=tarball,download_folder="downloadsv1"))
    os.system('touch downloadsv1/success')
except Exception as e:
    os.system('rm -rf downloadsv1')
    print(e)
    exit(-1)

downloaded_filesv2=[]
try:
    print("Downloading V2 Tarballs from aws")
    for tarball in TARBALLSv2:
        tarball=tarball.replace("\n", "")
        downloaded_filesv2.append(fetch_aws_file(bucket=AWS_BUCKET,filepath=tarball,download_folder="downloadsv2"))
    os.system('touch downloadsv2/success')
except Exception as e:
    os.system('rm -rf downloadsv2')
    print(e)
    exit(-1)

print("Generating packages list for v1")
file_path = "packages_listv1"
with open(file_path, 'w') as pfile:
    for f in downloaded_filesv1:
        tar=tarfile.open(f)
        for member in tar.getmembers():
            if member.name.count('/') == 1:
                pfile.write(member.name+"\n")
    pfile.close()

print("Generating packages list for v2")   
file_path = "packages_listv2"
with open(file_path, 'w') as pfile:
    for f in downloaded_filesv2:
        tar=tarfile.open(f)
        for member in tar.getmembers():
            if member.name.count('/') == 1:
                pfile.write(member.name+"\n")
    pfile.close()


    
    

