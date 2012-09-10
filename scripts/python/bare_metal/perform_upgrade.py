import os
import os.path
import subprocess

# Change to the workspace directory
os.chdir('/var/lib/jenkins/workspace')

# Run git command to print current commit hash
subprocess.call(['git', 'log', '-1'])

# Run Things
print "!!## -- Performing Upgrade on Bare Metal -- ##!!"