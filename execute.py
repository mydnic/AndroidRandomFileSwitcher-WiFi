import paramiko, random, os
from config import *

# Prepare Command
rawcommand = 'find {path} -name {pattern}'
command = rawcommand.format(path=filePath, pattern=fileExtension)

# Connect to Android Device
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port=port, username=username, password=password)

# List the distant files and chose a random one
distantFiles = list()

stdin, stdout, stderr = ssh.exec_command(command)
filelist = stdout.read().splitlines()

ftp = ssh.open_sftp()
for afile in filelist:
    (head, filename) = os.path.split(afile)
    distantFiles.append(filename)

chosenDistantFile = random.choice(distantFiles)

# List the local files and chose a random one
localFiles = list()

def mp3gen():
    for root, dirs, files in os.walk(localPath):
        for filename in files:
            if os.path.splitext(filename)[1] == fileExtension:
                yield os.path.join(root, filename)

for mp3file in mp3gen():
    localFiles.append(mp3file)

chosenLocalFile = random.choice(localFiles)

print 'we will delete', chosenDistantFile, ' and replace with', chosenLocalFile
