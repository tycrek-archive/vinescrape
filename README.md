# vinescrape
A python script to download all of Vines currently public videos (WIP)

# Note: I do not have every Vine downloaded yet. It is still in progress. I will update this repo when they have been downloaded.

## Intro

I wanted to download all Vines that are currently on the Vine website because the so-called Archive isn't actually functioning.

This script only gets Vines that are still public. I got the list of links from [this web index](https://vine.inkdroid.org/archive/). The archive contains over 127 million links, which I have estimated to total around 122 terabytes. I am uploading them to my unlimited [OpenDrive](http://opendrive.com/).

This is primarily more of a personal project, so I'm not really going to be providing support for setting up the script. If you can figure it out on your own, try it! I did however provide basic steps below.

## I want to try it!

Cool. Download [these archives](https://vine.inkdroid.org/archive/) and extract them. In `filelist.txt`, replace my path with wherever you have them saved (Sublime Text is good at doing replacing lots of stuff). Use Python 3 and install `youtube_dl` with `pip install`. I have provided `rclone.exe`. Read the [rclone docs](https://rclone.org/) to figure out how to set it up. In the script, change where rclone points to on the remote server.

Run the script with Python in your terminal. **It will take a very long time**. It will also *destroy* your Internet data plan, so make sure you have an unlimited data plan before running for good! Also, the largest links file contains around 61 GB of Vines, so make sure you have at least that much free space (you don't need terabytes upon terebytes because after each link file is downloaded, it moves the videos to OpenDrive and deletes them from your disk. To keep the videos, change `move` to `copy` in the rclone command).

Make sure to remove everything from `scraped/_ydl.txt` to make sure you actually download stuff.

## Credits and thanks

- Ricardo Garcia Gonzalez (Creator of youtube-dl)
- Nick Craig-Wood (Creator of rclone)
- Everyone at StackOverflow

Special thanks to Ed Summers (https://github.com/edsu) for the link archive.