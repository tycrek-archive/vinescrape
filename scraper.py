##  vinescraper by Joshua Moore (github.com/tycrek)
##  Python 3
##  Special thanks to Ed Summers (https://github.com/edsu) for the link archive
## Credits:
##  Jason Huggins 				(Creator of Selenium)
##  Ricardo Garcia Gonzalez 	(Creator of youtube-dl)
##  Mozilla Foundation			(for geckodriver.exe)
##  Nick Craig-Wood				(Creator of rclone)
##  Everyone at StackOverflow

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import os.path
import time
import json
import youtube_dl
import subprocess

# Use Selenium to scrape the Vine archive JSON file for a given ID
# Param: url: the URL to scrape
# It attempts a scrape 5 times before moving on
def scrapeURL(url):
	for i in range(5):
		try:
			# Run Selenium with Firefox (geckodriver.exe)
			driver = webdriver.Firefox(firefox_options=options)

			# Set the driver timeout
			driver.set_page_load_timeout(5)

			driver.get(url)                           # Download the page with Selenium
			page = driver.find_element_by_id("json")  # Extract the JSON element
			data = json.loads(page.text)              # Parse our JSON data
			videoURL = data['videoUrl'].split("?")[0] # Extract the video URL and remove "version"
			info = dict()                             # Metadata storage
			info['username']    = data['username']
			info['description'] = data['description']
			info['created']     = data['created']
			info['likes']       = data['likes']
			info['reposts']     = data['reposts']
			info['loops']       = data['loops']

			# Close the current browser session
			driver.close()

			return videoURL, info
		except Exception as e:
			print(e)
			print("Failed, retrying! Try " + str(i))
	print("! Full failure!")


options = Options()                 # Option set for running Selenium
options.set_headless(headless=True) # Run in background



filelist = open('filelist.txt', 'r+') # The list of files containing links
files = filelist.readlines()
filelist.close()

filecount = 0 # Keep track of which file we are on
for file in files:
	print("* File " + str(filecount) + " of " + str(len(files)))

	file = file.rstrip("\n") # Remove trailing newlines from the filename

	links = [] # Store the links here

	# Read the file and add the links to links[]
	with open(file, 'r+') as f:
		for line in f.readlines():
			# Clean up the link to only get the ID
			link = line.split(" ")[1].rstrip("\n\r").replace("/card?api=1", "").split("/")[-1]
			
			# Add the JSON link to links[]
			links.append("https://archive.vine.co/posts/" + link + ".json")


	print("\n\n! ! ! DOWNLOADING ! ! !")

	linkcount = 0 # Keep track of which link we are on
	for link in links:
		# Extract the link ID from the URL
		linkid = link.split("/")[-1].replace(".json", "")

		print("\nScraping " + linkid + " (" + str(linkcount) + " of " + str(len(links)) + ")...")
		
		# Check to see if the link has already been scraped
		if os.path.isfile(linkid):
			print("! Link already scraped, skipping!")
			continue

		# Attempt to download the video and metadata from the JSON link
		try:
			vineVideo, vineInfo = scrapeURL(link)
			vineInfo['id'] = linkid

			# Set our youtube-dl options
			ydl_opts = {
				"outtmpl": "./archive/videos/{}.%(ext)s".format(linkid),
				"quiet": "true",
				"download_archive": "scraped/_ydl.txt"
			}

			# Attempt to download the video and save it
			with youtube_dl.YoutubeDL(ydl_opts) as ydl:
				ydl.download([vineVideo])

			# Write the metadata to a JSON file
			with open("archive/" + linkid + ".json", 'w') as outfile:
				json.dump(vineInfo, outfile, indent=4, sort_keys=True)

			# Place an indicator file in scraped so we know to not download again
			f = open("scraped/" + linkid, "w+")
			f.close()

			print("Link " + linkid + " scraped")
		except:
			print("! Failed to scrape " + linkid + "!")

		# Upload to OpenDrive
		print("\nUploading " + linkid + " (" + str(linkcount) + " of " + str(len(links)) + ")...")
		
		# Use rclone to upload the .mp4 and .json files to OpenDrive
		try:
			# Use Python subprocess to run a system command
			subprocess.run(['rclone move archive/videos/' + linkid + '.mp4 remote:VINE_REBORN/archive/videos/'],shell=True)
			subprocess.run(['rclone move archive/' + linkid + '.json remote:VINE_REBORN/archive/'],shell=True)			
			
			print("Link " + linkid + " uploaded")
		except Exception as e:
			print(e)
		linkcount += 1


	'''print("\n\n! ! ! UPLOADING ! ! !")

	linkcount = 0
	## Upload all from current file to OpenDrive
	## (I am aware there are two  link in links  loops,
	##  this is intentional.)
	for link in links:
		# Extract the ID from the URL
		linkid = link.split("/")[-1].replace(".json", "")

		print("\nUploading " + linkid + " (" + str(linkcount) + " of " + str(len(links)) + ")...")
		
		# Use rclone to upload the .mp4 and .json files to OpenDrive
		try:
			# Use Python subprocess to run a system command
			subprocess.run(['rclone move archive/videos/' + linkid + '.mp4 remote:VINE_REBORN/archive/videos/'],shell=True)
			subprocess.run(['rclone move archive/' + linkid + '.json remote:VINE_REBORN/archive/'],shell=True)			
			
			print("Link " + linkid + " uploaded")
		except Exception as e:
			print(e)
		linkcount += 1'''

	filecount += 1

driver.quit() # Close out all Selenium processes

print("\n\nProcess complete. Vine has been saved!")