from common import *
from base import *
class Parent(Base):
    def __init__(self):
        super().__init__()
        self.repo_url="ssh://git@github.com:22/MentorEmbedded/mel-manifest.git"
        self.repo_branch="master"
        self.mirrorlocation="http://easource.alm.mentorg.com/sources/"
        self.syncsourcesto="easource.alm.mentorg.com:/opt/sources/"
        self.sstate_mirror="http://easource.alm.mentorg.com/sstate"
        self.preamble="/mnt/systembuilder/build/scripts/jenkins_preamble"
        self.systembuilder="/mnt/systembuilder"
        self.mgls_license_file="8224@svr-alm-eng-03.alm.mentorg.com"
        self.jenkinspreamble="/mnt/systembuilder/build/scripts/jenkins_preamble"

        self.shortid=os.getenv('shortid')
        if self.shortid==None:
            print('Environment variable shortid missing')
            exit(-1)
        
        self.machine=os.getenv('machine')
        if self.machine==None:
            print('Environment variable "machine" missing')
            exit(-1)

        self.base_version=os.getenv('base_version')
        if self.base_version==None:
            print('Environment variable "base_version" missing')
            exit(-1)

        
    def checkout(obj):
        os.chdir(obj.workspace)
        repo_url=obj.repo_url
        repo_branch=obj.repo_branch
        manifest=obj.manifest
        os.system('mkdir -p repotop')
        os.chdir('repotop')
        sh('repo init -u '+repo_url+' -b '+repo_branch+' -m '+manifest+' --current-branch')
        sh('repo sync -d -c -q --jobs=10')
        sh('repo manifest -o - -r')
        os.chdir('./.repo/manifests')
        sh('git rev-parse HEAD',showoutput=1)

    def fetch_and_untar_repotop(obj):
        os.chdir(obj.workspace)
        ash(obj.jenkinspreamble+" untar")
       
    def install_toolchain(obj):
        os.chdir(obj.workspace)
        with open(r'repotop/scripts/jenkins_mel', 'r') as file:
            data = file.read()
            data = data.replace('# configure build folder to build image', 'exit 0\n')
            with open(r'jenkins_mel', 'w') as file:
                file.write(data)
        
        sh('chmod a+x jenkins_mel',showoutput=1)
        ash('./jenkins_mel')

    
    def configure(obj):
        os.chdir(obj.workspace)
        
        machine=obj.machine
        workspace=obj.workspace
        with open(r'repotop/scripts/jenkins_mel', 'r') as file:
            data = file.read()
            data=replace_nth(data, "install_tools", "", 2)
            data = data.replace('add_image_features "${build_image_features}"', 'exit 0\n')
            with open(r'jenkins_mel', 'w') as file:
                file.write(data)
        sh('chmod a+x jenkins_mel')
        ash('./jenkins_mel')

        with open(r'build_'+machine+"/conf/local.conf", 'r') as file:
            data = file.read()
            #print(data)
            data += 'INHERIT += "archiver"\n'
            data += 'BB_GIT_SHALLOW = "0"\n'
            data += 'ARCHIVER_MODE[src] = "original"\n'
            data += 'TOOLCHAINS_PATH = "'+workspace+'/toolchain/toolchains"'
            with open(r'build_'+machine+"/conf/local.conf", 'w') as file:
                file.write(data)
                file.close()
        os.chdir(obj.workspace)
    
    def fetch_sources(obj):
        os.chdir(obj.workspace)
        sbmount=obj.systembuilder
        base_build_name=obj.base_build_name
        shortid=obj.shortid
        machine=obj.machine
        
        difffile="ossdiff_"+machine+"_mel.txt"
        sh('cp '+sbmount+"/"+base_build_name+"/"+shortid+"/"+difffile+" .")
        packages={}
        with open(difffile, 'r') as file:
            lines = file.readlines()
            for line in lines:
                package_name=line.split(",")[0]
                packages[package_name]=package_name
                
        for key in packages:
            package=packages[key]
            os.chdir('build_'+machine)
            ash("bitbake -c ar_original "+package)
            ash("bitbake -f -c deploy_archives "+package)

    def upload_sources(obj):
        os.chdir(obj.workspace)
        machine=obj.machine
        shortid=obj.shortid
        sbmount=obj.systembuilder
        base_build_name=obj.base_build_name

        source_directory='build_'+machine+"/tmp/deploy/sources"
        archive_name="sources_"+machine+".tar.gz"
        cmd='tar -zcvf '+archive_name+' '+source_directory
        sh(cmd)
        
        sh('cp '+archive_name+" "+sbmount+"/"+base_build_name+"/"+shortid+"/"+archive_name)