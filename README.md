<!-- TABLE OF CONTENTS -->
## Table of Contents

* [Description](#Description)
* [Prerequisites](#Prerequisites)
* [How to set up Memebot](#How-to-set-up-Memebot)
* [Viewing information](#Viewing-information)

# Description
- This bot uses the requests module to grab posts from the hot page of a subreddit and posts the one with the highest number of upvotes to Instagram with the original title as the caption using the instabot library.

# Prerequisites
- Raspberry Pi

# How to set up Membot
Log in to raspberry via ssh or open terminal on raspberry pi
1. Download repository
```sh
git clone https://github.com/Kyle678/instaMemebot.git
```
2. Change username and password in bot.py to sign into Instagram
```python
bot.login(username='username',password='password')
```
3. Edit hashtags and subs variables near the top of bot.py
```python
hashtags=['hashtag1','hashtag2'] # leave empty if none are wanted
subs=['subreddit1','subreddit2']
```
4. Change shortestTime and LongestTime variables at the top of bot.py
   - This is the time that the bot will wait before making another post
     - Time is in seconds and is set to 4-6 hours by default
```python
shortestTime=60**2*4 # 4 hours
longestTime=60**2*6 # 6 hours
```
5. Run Memebot.py
   - Running this launches the task in the background so you're free to disconnect if using a remote terminal

# Viewing information
- After setting up and starting Memebot, run viewMemebot.py to see the time for the next post as well as a clock counting down
```sh
Next meme will post at 7:09:33 pm
Time remaining: 1:35:33.158757
```
- Navigate to data/pictures/ to view any images that have been uploaded to Instagram

# Extra information
- Running Memebot.py while process is already active will restart Memebot
- Memebot posts something when it is first run and then waits x amount of time before posting again

<!-- LICENSE -->
## License

Distributed under the MIT License