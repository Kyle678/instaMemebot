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

# How to set up Membot
Log in to raspberry via ssh or open terminal on raspberry pi
1. Download repository
```sh
git clone https://github.com/Kyle678/instaMemebot.git
```
2. Open Memebot.ini to configure Memebot
   - Under userinfo input your username and password
   ```sh
   [userinfo]
   username=username
   password=password
   ```
   - Under preferences add hashtags to put in caption and subreddits to scrape pictures from
   ```sh
   [preferences]
   hashtags=hashtag1,hashtag2 # put None if hashtags are undesired
   subreddits=subreddit1,subreddit2
   ```
   - Enter the minimum and maximum times you want the bot to pause after each post in seconds. Default is 4-6 hours.
   ```
   shortestTime=14400 # 4 hours 
   longestTime=21600
   ```
3. Run Memebot.py
   - Running this launches the task in the background so you're free to disconnect if using a remote terminal
4. Let Memebot run
   - Memebot will run as long as you have a steady internet connection
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

<!-- LICENSE -->
## License

Distributed under the MIT License