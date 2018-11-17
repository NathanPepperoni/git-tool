import subprocess, os

class InShellGitUtility:
    
    __DEFAULT_EDITOR = '"vim"'
    __PREVIOUS_EDITOR = __DEFAULT_EDITOR    

    def makeBackupBranch(self):
        self.__makeShellCall(['git', 'branch', '-D', 'autosquash_save_branch'])
        output = self.__makeShellCall(['git', 'branch', 'autosquash_save_branch'])
        error_info = str(output[1])[2:-1]
        if (len(error_info) > 1):
            return False
        return True
    
    def setSequenceEditor(self, sequence_editor):
        self.__PREVIOUS_EDITOR = self.getCurrentEditor()
        self.__makeShellCall(['git', 'config', 'sequence.editor', [sequence_editor]])
        
    def revertSequenceEditor(self):
        if (self.__PREVIOUS_EDITOR == "UNSET"):
            self.__unsetSequenceEditor()
        else:
            self.__makeShellCall(['git', 'config', 'sequence.editor', [self.__PREVIOUS_EDITOR]])

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
            return False
        if (log_entry.count("Author: ") == 0):
            return False
        if (log_entry.count("Date: ") == 0):
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
    
    def __makeShellCall(self, call):
        process = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return process.communicate()

class LogEntry:
    def __init__(self, commit_hash, author, commit_message, is_merge):
        self.commit_hash = commit_hash
        self.author = author
        self.commit_message = commit_message
        self.is_merge = is_merge 