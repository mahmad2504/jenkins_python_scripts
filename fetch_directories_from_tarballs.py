#! /usr/bin/python
import os
import subprocess
import sys

def fetch_aws_file(file_path):
    cmd_str="aws s3 cp "+file_path
    output = subprocess.check_output(cmd_str, shell=True)

bucket="filesend.eps.mentorcloudservices.com"
tarballs_toprocess=[
"/INDLIN/releases/industrial-os-2.4.1/oss/base-runtime.tar.gz",
"/INDLIN/releases/industrial-os-2.4.1/oss/ipc-runtime.tar.gz"]


print("Hello world")