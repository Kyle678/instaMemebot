from instabot import Bot
import os,requests,shutil,random,time,datetime,json,configparser
from PIL import Image,ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES=True

url='https://gateway.reddit.com/desktopapi/v1/subreddits/{}?rtj=only&redditWebClient=web2x&app=web2x-client-production&allow_over18=1&include=identity%2CstructuredStyles%2CprefsSubreddit&geo_filter=US_CA&layout=card'

headers={'authority': 'gateway.reddit.com',
'method': 'GET',
'scheme': 'https',
'accept': '*/*',
'accept-encoding': 'gzip, deflate, br',
'accept-language': 'en-US,en;q=0.9',
'cache-control': 'no-cache',
'content-type': 'application/x-www-form-urlencoded',
'origin': 'https://www.reddit.com',
'pragma': 'no-cache',
'reddit-user_id': 'desktop2x',
'referer': 'https://www.reddit.com/',
'sec-fetch-dest': 'empty',
'sec-fetch-mode': 'cors',
'sec-fetch-site': 'same-site',
'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}

def getHot(subs,keywords):
    """Grabs a list of meme data from a subreddit randomly picked from list subs"""
    choice=random.choice(subs) # picks random sub
    hoturl=url.format(choice) # formats url to request from
    headers['path']=hoturl[hoturl.find('/desktopapi'):] # adds destination to headers
    r=requests.get(hoturl,headers=headers) # sends request to server with hot posts from subreddit
    js=json.loads(r.text) # converts response into json to use
    return filterMemes(js,keywords)

def filterMemes(memes,keywords):
    """Filters out things like advertisements, videos, gifs, and any posts with specific keywords"""
    if keywords[0]=='None':keywords=[]
    notads=[x for x in memes['posts'].keys() if len(x)<12] # filters out ads
    for m in memes['posts'].keys():
        post=memes['posts'][m]
        if any(word in post['title'].lower().split(' ') for word in keywords):continue
        if post['media'] and 'resolutions' in post['media'].keys() and post['id'] in notads and 'reddit' not in post['title'].lower(): # checks for required info and filters out posts about reddit
            newmeme={'id':post['id'],'comments':post['numComments'],'upvotes':post['score'],'title':post['title']} # creates dict object for meme to post
            urls=post['media']['resolutions'][0]['url'] # gets url for picture
            newmeme['picurl']=urls[:urls.find('?')].replace('preview','i') # converts it to full size image url
            if 'external' not in newmeme['picurl'] and ('jpg' in newmeme['picurl'] or 'jpeg' in newmeme['picurl'] or 'png' in newmeme['picurl']): # adds memes with type jpg or png
                memes.append(newmeme)
    return memes

def downloadPicture(url):
    """Downloads meme image and saves it to a permanent folder as well as temp folder so it can upload"""
    print('Downloading '+url)
    temppath=os.path.join('data','temp','pic.jpg')
    datefolder=str(datetime.date.today())
    path=os.path.join('data','pictures',datefolder)
    if not os.path.exists(path):os.mkdir(path) # creates folder named as the date to save pictures
    name=url.split('/')[-1] # gets file extension
    fullpath=os.path.join(path,name).replace('png','jpg')
    r=requests.get(url,stream=True) # downloads picture
    if r.status_code==200:
        r.raw.decode_content=True
        with open(temppath,'wb') as f:
            shutil.copyfileobj(r.raw,f) # writes picture to file
        Image.open(temppath).convert('RGB').save(fullpath) # copies picture to permanent folder
        return temppath
    else:
        print('failure')

def generateHashtags(hashtags):
    """return list of hashtags in random order from list"""
    s=''
    if hashtags[0]=='None':return s
    choices=list(range(len(hashtags)))
    while choices:
        c=random.choice(choices) # chooses random hashtag to add
        s+=' #'+hashtags[c]
        choices.remove(c)
    return s

def chooseMeme(memes,limit=10):
    """Picks meme with highest amount of upvotes from list and returns it"""
    print('Choosing Meme . . .')
    if len(memes)<limit: # changes iteration limit to amount of memes in list
        limit=len(memes)
    with open(os.path.join('data','archive.txt'),'r') as file:
        archive=file.readline().split(';') # creates list of previous posts
    s=sorted(memes,key=lambda x:x['upvotes']) # sorts list of memes by upvotes
    p=s[-1] # chooses meme with highest number of upvotes
    while p['id'] in archive: # chooses next meme if current meme has already been posted
        try:
            p=s[s.index(p)-1]
        except:
            return None # returns nothing if it hits the end of the list
    return p

def processMeme(meme):
    """Downloads meme, corrects any compatibility issues with size or aspect ratio, and archives the id of the post. Returns path and title to meme."""
    print('Processing')
    time.sleep(1) # waits after downloading webpage
    name=downloadPicture(meme['picurl'])
    fixPicture(name)
    with open(os.path.join('data','archive.txt'),'a') as file:
        file.write(meme['id']+';') # writes id of meme to archive
    return name,meme['title']

def cleanUp():
    """Clears temp folder"""
    tempfolder=os.path.join('data','temp')
    if os.listdir(tempfolder):
        for file in os.listdir(tempfolder):
            os.remove(os.path.join(tempfolder,file)) # removes any files currently in the temp folder

def fixPicture(path):
    """Fixes image based on instagram picture restrictions"""
    with Image.open(path) as im:
        x,y=im.size
        if x<1080: # Width of photo must be at least 1080p
            print('Enlarging')
            y*=round(1080/x) # uniformly changes y value
            x=1080
            im=im.resize((x,y)) # resizes photo
            im.save(path)
            x,y=im.size
        if x/y>1.91 or x/y<.8: # Aspect ratio must be >= 0.8 and <= 1.91
            print('Correcting aspect ratio')
            ox,oy=x,y
            while x/y>1.91:y+=1 # Increases value until minimum is met
            while x/y<.8:x+=1
            hx=round((x-ox)/2)
            hy=round((y-oy)/2)
            result=Image.new(im.mode,(x,y),(0,0,0)) # Pads photo with black rectangles if aspect ratio is changed
            result.paste(im,(hx,hy)) # pastes rectangle behind picture
            result.save(path)
    
def uploadMeme(path,caption,hashtags,username,password):
    """Uploads meme to instagram"""
    if not os.path.exists(path):
        return # returns if picture isn't found
    print('Uploading . . .')
    bot=Bot()
    bot.login(username=username,password=password) # logs into Instagram with api
    caption+=generateHashtags(hashtags) # adds hashtags to caption
    info=bot.upload_photo(path,caption=caption) # uploads picture with caption
    if info:print('Picture uploaded')

def setup():
    """If required files/folders don't exist, creates them"""
    paths=['data',os.path.join('data','pictures'),os.path.join('data','temp')]
    for f in paths:
        if not os.path.exists(f):
            os.mkdir(f)
    texts=[os.path.join('data',x)for x in ['archive.txt','errors.txt']]
    for f in texts:
        if not os.path.exists(f):
            file=open(f,'w');file.close()
    with open('data/pid.txt','w') as file:
        file.write(str(os.getpid()))
    cleanUp()

def loadConfig():
    """Loads configuration file"""
    config=configparser.ConfigParser()
    config.read('Memebot.ini')
    username=config['userinfo']['username']
    password=config['userinfo']['password']
    pref=config['preferences']
    keywords=pref['keywords'].split(',')
    shortestTime,longestTime=int(pref['shortestTime']),int(pref['longestTime'])
    hashtags,subs=pref['hashtags'].split(','),pref['subreddits'].split(',')
    if not subs:
        print('No subreddits are listed') # ends if subs is empty
        raise SystemExit
    return  username,password,keywords,shortestTime,longestTime,hashtags,subs

def wait(shortestTime,longestTime):
    """Randomly wait before next post for between shortestTime to longestTime"""
    t=random.randrange(shortestTime,longestTime) # chooses random time between shortestTime and longestTime
    now=datetime.datetime.now() # records time and date
    ne=now+datetime.timedelta(0,t) # calculates time of next post
    until=ne-now # calculates time until next post
    with open(os.path.join('data','time.txt'),'w') as file:
        file.write(str(ne.time())) # writes time of next post to time.txt
    cleanUp()
    print('Next meme scheduled for '+str(ne))
    while until.total_seconds()>0: # wait while time remaining is more than 0 seconds
        until=ne-datetime.datetime.now()
        time.sleep(.1)

def main():
    """Main method"""
    setup()
    while True:
        username,password,keywords,shortestTime,longestTime,hashtags,subs=loadConfig()
        try: # Catches any errors, writes them to errors.txt, and waits 1 minute before trying again
            memes=getHot(subs,keywords)
            meme=chooseMeme(memes)
            if not meme:continue # If no meme is returned, restarts process
            path,title=processMeme(meme)
            uploadMeme(path,title,hashtags,username,password)
            wait(shortestTime,longestTime)
        except Exception as e:
            with open('data/errors.txt','a') as file:
                file.write(str(datetime.datetime.now())+'\n'+str(e)+'\n')
            time.sleep(60)

if __name__=='__main__':
    main()