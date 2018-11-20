import sys, subprocess, os
from gitutils import InShellGitUtility, LogEntry

MOCK_AUTO_SEQUENCE_EDITOR = '"sed -i -e \'1 ! s/pick/pick/g\'"'
AUTO_SEQUENCE_EDITOR = '"sed -i -e \'1 ! s/pick/fixup/g\'"'
REBASE_SUCCESS_MESSAGE = "Successfully rebased and updated "
BACKUP_BRANCH_NAME = "autosquash_save_branch"
PREFIX = "\n    "

git_utility = InShellGitUtility()

def getSquashCount():
    branch_name = sanitizeBranchName(git_utility.getCurrentBranchName())
    count = 0
    log_entries = git_utility.getLogEntries()
    for entry in log_entries:
        count+=1
        message_before_whitespace = entry.commit_message.split()[0]
        if (message_before_whitespace.lower().count(branch_name)):
            return count
    return -1
        
def sanitizeBranchName(branch_name):
    return branch_name.lower().replace("feature/", '')

def consolePrint(message):
    print(PREFIX + message)

def makeBackupBranch():
    backup_branch_success = git_utility.makeBackupBranch(BACKUP_BRANCH_NAME)
    if (not backup_branch_success):
        return False
    return True
    
        
if __name__ == '__main__':
    os.chdir("C:\\dummy-repo")
    
    if (sys.version_info[0] < 3):
        consolePrint("This script only works with python version 3")
        raise SystemExit()
    
    squash_count = getSquashCount()
    if (squash_count < 0):
        consolePrint("error message about log parsing")
        raise SystemExit()
    
    if (not makeBackupBranch()):
        consolePrint('error message about backup branch creation')
        raise SystemExit()
    consolePrint("successfully made backup branch: " + BACKUP_BRANCH_NAME) 
    
    git_utility.setSequenceEditor(MOCK_AUTO_SEQUENCE_EDITOR)
    rebase_info = git_utility.rebaseWithHeadOffset(squash_count)
    git_utility.revertSequenceEditor()
    
    if (rebase_info[:len(REBASE_SUCCESS_MESSAGE)] == REBASE_SUCCESS_MESSAGE):
        consolePrint("rebase successful!")
        raise SystemExit()
    else:
        consolePrint("couldn't rebase successfully")
        raise SystemExit()