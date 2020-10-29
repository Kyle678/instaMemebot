import os,psutil

def main():
    """Starts/restarts Memebot"""
    try:
        with open(os.path.join('data','pid.txt')) as file:
            latest=int(file.readline()) # gets most recent pid used by memebot
    except:
        latest=None # set to none if not found
    if latest:
        for proc in psutil.process_iter():
            if proc.pid==latest:
                os.system('kill -kill '+str(proc.pid)) # kills process if running
                break
    os.system('nohup python3 bot.py &') # starts memebot in background with output bound to nohup.out

if __name__=='__main__':
    main()