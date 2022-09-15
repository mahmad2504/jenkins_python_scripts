from common import *
class Base:
    params={}
    def __init__(self,params):
        print(params)
        if "PATH" in params:
            params['PATH']=params['PATH']+":"+sh('echo $PATH').strip()
        else:
            params['PATH']=sh('echo $PATH').strip()
        
        
        pwd=sh('pwd').strip()
        print(params['WORKSPACE'])
        if pwd != params['WORKSPACE']:
            print('Current directory does not match with WORKSPACE env variable')
            exit(-1)


        printdictionary(params,'Parameters')
    
        
        
        
