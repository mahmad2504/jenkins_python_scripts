from common import *
class Base:
    def __init__(self):
        print("base class")
        self.workspace=os.getenv('workspace')
        self.path=os.environ['PATH']
        print('Executing Script in '+self.workspace)
       
        if self.workspace == None:
            print('Environemntal variable "workspace" is missing')
            exit(-1)

        if os.getcwd() != self.workspace:
            print('Current directory does not match with WORKSPACE env variable')
            exit(-1)
        os.environ["workspace"]=self.workspace
        os.environ["WORKSPACE"]=self.workspace
        
        
        
