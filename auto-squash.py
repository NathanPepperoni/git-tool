import subprocess, os

os.chdir("C:\\dummy-repo\\")

def add():
    process = subprocess.Popen(["git", "add", "-u"], stdout=subprocess.PIPE, shell=True)
    output = process.communicate()[0]
    print(output)

def commit():
    process = subprocess.Popen(["git", "commit", "-m", "s"], stdout=subprocess.PIPE, shell=True)
    output = process.communicate()[0]
    print(output)

def rebase():
    process = subprocess.Popen(["git", "rebase", "-i", "HEAD"], stdout=subprocess.PIPE, stdin=subprocess.PIPE, shell=True)
    process.communicate("")
    output = process.communicate()
    print(output)
    

rebase()