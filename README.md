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

## ProductSetup
![](https://i.imgur.com/1eE02sb.gif)

Script to retrieve either trunk or STP product/target place them in the current directory. 
Trunk will retrieved by default, unless -STP is passed as an arguement

## Usage
To make the most of these scripts, it is recommended that you set up aliases in your .bashrc file (located in your user directory)

for example, if you cloned this repo directly on C: `alias product='python c:/git-tool/product-setup.py'`

you could then just type `product` or `product -STP` into the terminal as in the demo and have the script run in the terminal without having to specify a path each time.
