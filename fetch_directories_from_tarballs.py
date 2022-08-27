#! /usr/bin/python
import os
import subprocess
import sys

def fetch_aws_file(bucket,filepath,download_folder):
    filename=os.path.basename(filepath)
    if os.path.exists(download_folder+"/"+filename):
        print("Using cached copy of "+filename)
    else:
        print("Donloading "+filename)
        cmd="aws s3 cp s3://"+bucket+filepath+" "+download_folder+"/"
        subprocess.check_output(cmd, shell=True)
    return download_folder+"/"+filename

bucket="filesend.eps.mentorcloudservices.com"
download_folder="downloads"
tarballs_toprocess=[
"/INDLIN/releases/industrial-os-2.4.1/oss/siemens-runtime.tar.gz",
"/INDLIN/releases/industrial-os-2.4.1/oss/ipc-runtime.tar.gz",
"/INDLIN/releases/industrial-os-2.4.1/oss/base-runtime.tar.gz"]
downloaded_files=[]
os.system('mkdir -p scratch')
try:
  print("Fetching Tarballs from aws")
  for tarball in tarballs_toprocess:
      downloaded_files.append(fetch_aws_file(bucket,tarball,download_folder))
except Exception as e:
   print(e)

try:
  for tarball in downloaded_files:
     print("Processing "+tarball)
     cmd='tar -xvf '+tarball+' -C scratch'
     subprocess.check_output(cmd, shell=True)
except Exception as e:
   print(e)

print("Done")