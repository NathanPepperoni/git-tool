TODO:

   better error logging

   increased count accuracy without sacrificing robustness

   refactor some of the code to be less janky

   maybe make another abstraction layer between InShellGitEditor and the subprocess module?

   make a nice readme

   add tests
   
   document argument options

## AutoSquash
![](https://i.imgur.com/LxPomxw.gif)

Script to automate common git squash commands. Will automatically identify the latest commit with the same name as your current branch, and squash all later commits into it. A backup branch is made before modifying anything is altered in the current branch, so recovery is not possible. If a backup branch is unable to be created and validated, the squash will not proceed.