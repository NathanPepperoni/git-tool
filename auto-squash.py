import sys, subprocess, os
from gitutils import InShellGitUtility, LogEntry

MOCK_AUTO_SEQUENCE_EDITOR = '"sed -i -e \'1 ! s/pick/pick/g\'"'
AUTO_SEQUENCE_EDITOR = '"sed -i -e \'1 ! s/pick/fixup/g\'"'
REBASE_SUCCESS_MESSAGE = 'Successfully rebased and updated '
BACKUP_BRANCH_NAME = 'autosquash_save_branch'
PREFIX = '\n    '
IS_QUICK_SQUASH = False
IS_SAFE_SQUASH = False #not yet implemented
ARG_SQUASH_COUNT = -1

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
    consolePrint('error message about log parsing')
    raise SystemExit()
        
def sanitizeBranchName(branch_name):
    return branch_name.lower().replace('feature/', '').replace('fix/', '')

def consolePrint(message):
    print(PREFIX + message)

def makeBackupBranch():
    backup_branch_success = git_utility.makeBackupBranch(BACKUP_BRANCH_NAME)
    
    if (not backup_branch_success):
        consolePrint('error message about backup branch creation')
        raise SystemExit()
    consolePrint('successfully made backup branch: ' + BACKUP_BRANCH_NAME)  

def validateAndPopulateArgs():
    if (sys.version_info[0] < 3):
        consolePrint('This script only works with python version 3')
        raise SystemExit()
    args = [arg.lower() for arg in sys.argv]
    
    if ('-qs' in args):
        global IS_QUICK_SQUASH
        IS_QUICK_SQUASH = True
        
    shortCount = '-c' in args
    if (shortCount or '-count' in args):
        count_command = '-c' if shortCount else '-count'
        index = args.index(count_command)
        global ARG_SQUASH_COUNT
        ARG_SQUASH_COUNT = int(args[index+1]) + 1
    
    if ('-safe' in args):
        global IS_SAFE_SQUASH
        IS_SAFE_SQUASH = True
        
def performRebase():
    git_utility.setSequenceEditor(AUTO_SEQUENCE_EDITOR)
    rebase_info = git_utility.rebaseWithHeadOffset(squash_count)
    git_utility.revertSequenceEditor()    
    
    if (rebase_info.find(REBASE_SUCCESS_MESSAGE) >= 0):
        consolePrint('rebase successful!')
    else:
        consolePrint('couldn\'t rebase successfully')
        consolePrint(rebase_info)
        raise SystemExit()    
        
if __name__ == '__main__':    
    validateAndPopulateArgs()
    
    makeBackupBranch()

    if (IS_QUICK_SQUASH):
        git_utility.makeQuickCommit('.')
    
    squash_count = ARG_SQUASH_COUNT if ARG_SQUASH_COUNT > 0 else getSquashCount()
    
    performRebase()
    SystemExit()