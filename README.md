# git-tool

#AutoSquash
Script to automate common git command sequences

TODO:

   better error logging

   increased count accuracy without sacrificing robustness

   refactor some of the code to be less janky

   maybe make another abstraction layer between InShellGitEditor and the subprocess module?

   make a nice readme

   add tests


#ProductSetup
Script to retrieve either trunk or STP product/target place them in the current directory. 
Trunk will retrieved by default, unless -STP is passed as an arguement


To make the most of these scripts, it is recommended that you set up aliases in your .bashrc file (located in your user directory)
for example, if you cloned this repo directly on C: alias autosquash='python c:/git-tool/auto-squash.py'