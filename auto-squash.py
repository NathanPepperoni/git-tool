import subprocess, os

AUTO_SEQUENCE_EDITOR = '"sed -i -e \'1 ! s/pick/pick/g\'"'
DEFAULT_EDITOR = '"vim"'
PREVIOUS_EDITOR = DEFAULT_EDITOR

def makeBackupBranch():
    output = makeShellCall(['git', 'branch', '-D', 'autosquash_save_branch'])
    print(output)
    output = makeShellCall(['git', 'branch', 'autosquash_save_branch'])
    print(output)

def setSequenceEditor():
    output = makeShellCall(['git', 'config', 'sequence.editor', [AUTO_SEQUENCE_EDITOR]])
    print(output)
    
def getCurrentEditor():
    print(makeShellCall(['git', 'config', '--list']))
    print(os.getcwd())
    
def revertSequenceEditor():
    makeShellCall(['git', 'config', 'sequence.editor', [PREVIOUS_EDITOR]])
    
def getLogEntries():
    entries = []
    output = makeShellCall(["git", "log"])
    for s in str(output[0]).split('commit '):
        if (s[:4] == '    '):
            entries.append(s[4:])
    return entries

def makeShellCall(call):
    process = subprocess.Popen(call, stdout=subprocess.PIPE, shell=True)
    return process.communicate()

class LogEntry:
    def __init__(self, commit_hash, author, merge_commit, commit_message):
        self.commit_hash = commit_hash
        self.author = author
        self.merge_commit = merge_commit 
        self.commit_message = commit_message
        
    def __init__(self, commit_hash, author, commit_message):
        self.__init__(self, commit_hash, author, False, commit_message)

os.chdir("C:\\dummy-repo")
getLogEntries()