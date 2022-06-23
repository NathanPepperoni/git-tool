import sys, subprocess, os
from gitutils import InShellGitUtility, LogEntry

MOCK_AUTO_SEQUENCE_EDITOR = "sed -i -e \'1 ! s/pick/pick/g\'"
AUTO_SEQUENCE_EDITOR = "sed -i -e \'1 ! s/pick/fixup/g\'"
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
        message_chunks = entry.commit_message.replace(' ', '-').split('-');
        if (len(message_chunks) < 2):
            continue
        message_before_whitespace = message_chunks[0] + '-' + message_chunks[1]
        if (message_before_whitespace == branch_name):
            consolePrint('Identified base commit: ' + str(entry.commit_message))
            return count
    consolePrint('Unable to find commit to squash into. Aborting.')
    raise SystemExit()
        
def sanitizeBranchName(branch_name):
    name_chunks = branch_name.split('-')
    sanitized_name = '-'
    return sanitized_name.join(name_chunks[0:2]) 

def consolePrint(message):
    print(PREFIX + message)

def makeBackupBranch():
    backup_branch_success = git_utility.makeBackupBranch(BACKUP_BRANCH_NAME)
    if (not backup_branch_success):
        consolePrint('Could not create backup branch. Aborting.')
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