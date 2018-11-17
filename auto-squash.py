import subprocess, os
from gitutils import InShellGitUtility, LogEntry

AUTO_SEQUENCE_EDITOR = '"sed -i -e \'1 ! s/pick/pick/g\'"'

git_utility = InShellGitUtility()

def getHeadCount():
    log_entries = git_utility.getLogEntries()
    
        

os.chdir("C:\\dummy-repo")

print(git_utility.getCurrentBranchName())

#getHeadCount
#try to make safety branch
#change editor
#rebase
#revert editor
#check for issues
#output to user

