from common import *
############################################################################
#Environment Variable that should be set for this script
#
#machine=imx6qsabresd-mel
#machine=imx6ullevk-mel
#shortid=220823_1053
#base_version=12.0.5
#workspace=/var/jenkins/mahmad/workspace
#############################################################################

def generate_oss_tarballs(obj):
    count=0
    try:
        build_folder=obj.systembuilder+"/"+obj.base_build_name+"/"+obj.shortid
        files=os.listdir(build_folder)
        for file in files:
            if "ossdiff" in file:
                count=count+1
    except:
        print('folder '+build_folder+' does not exist')
        exit(-1)
    if(count==0):
        print('no ossdiff files found in '+build_folder)
        exit(-1)
   
    obj.fetch_and_untar_repotop()
    obj.install_toolchain()
    obj.configure()
    obj.fetch_sources()
    obj.upload_sources()