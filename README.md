<!-- TABLE OF CONTENTS -->
## Table of Contents

* [Description](#Description)
* [Prerequisites](#Prerequisites)
* [How to set up Memebot](#How-to-set-up-Memebot)
* [Viewing information](#Viewing-information)
* [Extra information](#Extra-information)

# Description
- This bot uses the requests module to grab posts from the hot page of a subreddit and posts the one with the highest number of upvotes to Instagram with the original title as the caption using the instabot library.

# Prerequisites
- Raspberry Pi
- Python 3.6+

# How to set up Membot
Log in to raspberry via ssh or open terminal on raspberry pi
1. Download repository
```sh
git clone https://github.com/Kyle678/instaMemebot.git
```
2. Open Memebot.ini in the instaMemebot folder to configure Memebot
   - If on terminal
   ```sh
   cd instaMemebot
   nano Memebot.ini
   ```
   - Under userinfo input your username and password
   ```sh
   [userinfo]
   username=username
   password=password
   ```
   - Under preferences add keywords to filter posts with, hashtags to put in caption, and subreddits to scrape pictures from
   ```sh
   [preferences]
   keywords=None # None if you choose not to filter any posts out
   hashtags=hashtag1,hashtag2 # None if hashtags aren't wanted
   subreddits=subreddit1,subreddit2
   ```
   - Enter the minimum and maximum time you want the bot to pause for after each post in seconds. Default is 4-6 hours.
   ```
   shortestTime=14400 # 4 hours 
   longestTime=21600 # 6 hours
   ```
3. Run Memebot.py
   - Running this launches the task in the background so you're free to disconnect if using a remote terminal
4. Let Memebot run
   - Memebot will continue running for as long as you let it
   - Run stop.py to stop Memebot

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
- Although named Memebot you can easily use it to post things like cute animals, food, the sky, etc.
- Configuration variables will update each time a post is made so you can change them while Memebot runs

<!-- LICENSE -->
## License

Distributed under the MIT License