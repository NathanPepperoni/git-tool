import subprocess
import sys
import os
import urllib.request
import base64
import getpass
from gitutils import InShellGitUtility, LogEntry

__TARGET_TYPE_LENGTH = 7
__STP_URL = 'https://jenkins.cerner.com/revcycle/view/STP-Assembly/job/revenuecycle-core/job/revenuecycle.product/job/Ares-STP/lastSuccessfulBuild/execution/node/5/ws/revenuecycle-millennium/target/'
__TARGET_URL = 'https://jenkins.cerner.com/revcycle/view/Trunk-Assembly/job/revenuecycle-core/job/revenuecycle.product/job/master/lastSuccessfulBuild/execution/node/5/ws/revenuecycle-millennium/target/'
__URL = __TARGET_URL

__PRODUCT = 'https://github.cerner.com/revenuecycle-core/revenuecycle.product.git'
__BRANCH = 'master'

git_utility = InShellGitUtility()

def fetch_target_name(data):
    lindex = data.find('.target')
    rindex = lindex + __TARGET_TYPE_LENGTH
    while(data[lindex] != '"' and lindex > 1):
        lindex = lindex-1
    
    if (data[lindex] != '"'):
        print("error message about parsing")
    return data[lindex+1:rindex]

def fetchURL(url, auth_token):
    req = urllib.request.Request(url)
    req.add_header('Authorization', 'Basic ' + auth_token)
    
    return urllib.request.urlopen(req).read()        

def hiddenGetPass(message):
    sys.stdout.write(message)
    sys.stdout.flush()
    subprocess.check_call(["stty","-echo"])
    password = input()
    subprocess.check_call(["stty","echo"])
    print('\n')
    return password        

def getPass(message):
    try:
        return hiddenGetPass(message)
    except:
        return input("Unable to hide password. Ensure screen isn't visible: ")

def validateAndPopulateArgs():
    if (sys.version_info[0] < 3):
        consolePrint('This script only works with python version 3')
        raise SystemExit()
    args = [arg.lower() for arg in sys.argv]
    if ('-stp' in args):
        global __URL
        __URL = __STP_URL
        global __BRANCH
        __BRANCH = 'Ares-STP'       
        
def downloadTarget():
    credentials = ('%s:%s' % (input('username: '), getPass('password: ')))
    auth_token = base64.b64encode(credentials.encode('ascii')).decode('ascii')

    data = fetchURL(__URL, auth_token)
    
    target_name = fetch_target_name(data.decode("utf8"))
    
    with open(target_name, 'wb') as output_file:
        target = fetchURL(__URL+target_name, auth_token)
        output_file.write(target)
    print(target_name + " downloaded!")       
   
def cloneProduct():
    if (git_utility.cloneBranch(__PRODUCT, __BRANCH)):
        print('product cloned!')

if __name__ == '__main__':
    validateAndPopulateArgs()
    downloadTarget()
    cloneProduct()