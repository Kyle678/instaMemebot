import os,psutil

with open(os.path.join('data','pid.txt')) as file:
    pid=file.readline()
for process in psutil.process_iter():
    if process.pid==int(pid):os.system('kill -kill '+pid)