import datetime,time,os,psutil

def processes():
    """Returns list of running processes"""
    return [p.pid for p in psutil.process_iter()]

def getTime():
    """Returns time of next post"""
    with open('time.txt') as file:
        return file.readline()

def getPid():
    """Returns most recent process id of memebot"""
    with open('pid.txt') as file:
        return int(file.readline())

def isUploading():
    """Checks whether the bot is currently uploading a meme"""
    return bool(os.listdir('temp'))

def main():
    """Display time of next post and time remaining"""
    if not os.path.exists('data'):
        print('Could not find folder "data". Make sure this is running in the correct directory and Memebot is running')
    os.chdir('data')
    while True:
        while isUploading() and getPid() in processes():
            os.system('clear')
            print('Waiting for upload . . .')
            time.sleep(.1)
        waiting=True
        t=getTime()
        pid=getPid()
        then=datetime.datetime.now() # initializes object to use for time of next post
        while waiting:
            h,m,s=[round(float(x)) for x in t.split(':')] # gets hour, minute, and second of next post time
            td=datetime.timedelta(0,(h*60**2)+(m*60)+s) # converts to time change
            now=datetime.datetime.now()
            if s==60:s=59
            then=then.replace(hour=h,minute=m,second=s) # creates time object with time of next post
            rh=h%12 if h%12!=0 else 12
            label='pm'if h>11 else 'am'
            until=then-now # calculates time remaining
            while not isUploading() and pid in processes() and until.seconds>0:
                os.system('clear')
                print(f'Next meme will post at {rh}:%02d:%02d {label}'%(m,s))
                now=datetime.datetime.now() # updates current time
                until=then-now # update time until next post
                tr=until if until.days==0 else str(until)[str(until).rfind(' ')+1:] # removes '-1 days' if it exists
                print(f'Time remaining: {tr}')
                time.sleep(.2)
            if pid not in processes():
                print("Memebot doesn't seem to be running. Try restarting.")
                raise SystemExit
            print('Waiting for upload . . .')
            while os.listdir('temp'): # waits for temp folder to be cleared
                time.sleep(1)
            waiting=False
        
if __name__=='__main__':
    main()