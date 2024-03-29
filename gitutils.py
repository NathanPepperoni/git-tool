import subprocess, os

class InShellGitUtility:
    
    __DEFAULT_EDITOR = '"vim"'
    __PREVIOUS_EDITOR = __DEFAULT_EDITOR    
    
    def cloneBranch(self, repo_url, branchname):
        self.__makeShellCall(['git', 'clone', repo_url])
        repo_name= repo_url.split('/')[-1].replace('.git','')
        os.chdir(repo_name)
        output = self.__makeShellCall(['git', 'checkout', branchname])
        is_valid_output = output[1][:10].decode("utf-8") == "Already on" or output[1].decode("utf-8") == "Switched to a new branch '" + branchname + "'\n"
        return is_valid_output
    
    def makeQuickCommit(self, add_scope):
        self.__makeShellCall(['git', 'add', add_scope])
        self.__makeShellCall(['git', 'commit', '-m', '"s"'])

    def makeBackupBranch(self, branch_name):
        self.__makeShellCall(['git', 'branch', '-D', branch_name])
        output = self.__makeShellCall(['git', 'branch', branch_name])
        error_info = str(output[1])[2:-1]
        if (len(error_info) > 1):
            return False
        return True
    
    def setSequenceEditor(self, sequence_editor):
        self.__PREVIOUS_EDITOR = self.getCurrentEditor()
        self.__makeShellCall(['git', 'config', 'sequence.editor', sequence_editor])
        
    def revertSequenceEditor(self):
        if (self.__PREVIOUS_EDITOR == "UNSET"):
            self.__unsetSequenceEditor()
        else:
            self.__makeShellCall(['git', 'config', 'sequence.editor', self.__PREVIOUS_EDITOR])

    def __unsetSequenceEditor(self):
        self.__makeShellCall(['git', 'config', '--unset', 'sequence.editor'])                
        
    def getLogEntries(self):
        log_entries = []
        output = self.__makeShellCall(["git", "log"])
        trimmed_output = str(output[0])[9:-1]
        for log_entry in trimmed_output.split('\\ncommit '):
            if (self.__isValidLogEntry(log_entry)):
                log_entries.append(self.__createLogEntry(log_entry))
        return log_entries
                
    def __isValidLogEntry(self, log_entry):
        commit_hash = log_entry.split('\\n')[0]
        if (len(commit_hash) != 40):
            print("bad hash")
            return False
        if (log_entry.count("Author: ") == 0):
            print("bad author")
            return False
        if (log_entry.count("Date: ") == 0):
            print("bad date")
            return False
        return True
    
    def __createLogEntry(self, log_entry):
        log_pieces = log_entry.split('\\n')
        commit_hash = log_pieces[0]
        author = ""
        commit_message = ""
        is_merge = False
        for piece in log_pieces:
            if (piece[:7] == "Merge: "):
                is_merge = True
            if (piece[:8] == "Author: "):
                author = piece[8:]
            if (piece[:4] == "    "):
                commit_message = piece[4:]
        return LogEntry(commit_hash, author, commit_message, is_merge)

    def getCurrentEditor(self):
        output = str(self.__makeShellCall(['git', 'config', '--list'])[0])
        if (output.count("sequence.editor=")):
            for config in output.split('\\n'):
                if (config[:16] == "sequence.editor="):
                    return config[16:]
        return "UNSET"
    
    def getCurrentBranchName(self):
        output = str(self.__makeShellCall(['git', 'symbolic-ref', '--short', 'HEAD'])[0])
        return output[2:-3]
    
    def rebaseWithHeadOffset(self, head_offset):
        output = self.__makeShellCall(['git', 'rebase', '-i', 'HEAD~' + str(head_offset)])
        rebase_info = str(output[1])[2:-1]
        return rebase_info
    
    def __makeShellCall(self, call):
        process = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return process.communicate()

class LogEntry:
    def __init__(self, commit_hash, author, commit_message, is_merge):
        self.commit_hash = commit_hash
        self.author = author
        self.commit_message = commit_message
        self.is_merge = is_merge 