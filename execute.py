import paramiko, random, os
from config import *

# Prepare Command
rawcommand = 'find {path} -name {pattern}'
command = rawcommand.format(path=filePath, pattern=filePattern)

# Connect to Android Device
print 'Start Connexion...'
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port=port, username=username, password=password)
sftp = ssh.open_sftp()
print 'Connected.'

# List the distant files and chose a random one
print 'Listing all files from distant device...'
distantFiles = list()

stdin, stdout, stderr = ssh.exec_command(command)
filelist = stdout.read().splitlines()

for afile in filelist:
    (head, filename) = os.path.split(afile)
    distantFiles.append(filename)

chosenDistantFile = random.choice(distantFiles)
print chosenDistantFile, 'is the distant file that was randomly picked'

# List the local files and chose a random one
print 'Listing all local files...'
localFiles = list()

def fileLoop():
    for root, dirs, files in os.walk(localPath):
        for filename in files:
            if os.path.splitext(filename)[1] == fileExtension:
                yield os.path.join(root, filename)

for file in fileLoop():
    localFiles.append(file)

chosenLocalFile = random.choice(localFiles)
(chosenPath, chosenFilename) = os.path.split(chosenLocalFile)

print chosenFilename, 'is the local file that was randomly picked'

# Deleting Distan File
sftp.remove(filePath + '/' + chosenDistantFile)
print chosenDistantFile, 'has been deleted'

# Move new file to Distant Device
sftp.put(chosenLocalFile, filePath + '/' + chosenFilename)
print chosenFilename, 'has been transfered to your device'

# End Script
sftp.close()
ssh.close()
print 'See you soon bro'
