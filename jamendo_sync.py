#!/usr/bin/python3
# -*-coding:UTF-8 -*
# Script which parse the public playlists of a Jamendo user 
# and upload the music files in a local directory
# @author douze12
# @date 09/12/2014

#imports
from jamendoApi import *
import logging as log
import os
import sys
import urllib.request


# Constants
curDir = os.path.dirname(__file__)
configFile=curDir+"/conf"
configKeys=["jamendoUrl","clientId","userName","destDir"]
delimiter=";"
logFile=curDir+"/.log"
logLevel=log.DEBUG
logFormat='%(asctime)s %(levelname)s - %(message)s'
playlistLimit=10

#log configuration
log.basicConfig(filename=logFile,level=logLevel, format=logFormat)


log.info("Begin")

def extractConfig():
	
	config = dict()
	
	file=open(configFile,"r")
	for line in file:
		tab = line.strip().split("=")
		config[tab[0]] = tab[1]
		log.debug("Config : "+line.strip())
	
	file.close()
	
	checkConfig(config)
		
	return config

# Method that check if the configuration is correct
def checkConfig(config):
	for key in configKeys:
		#test if all the configs are set
		if not key in config:
			errorMsg="Config ["+key+"] is not present in the configuration file"
			log.error(errorMsg)
			raise Exception(errorMsg)
		
		#test if the config is not empty
		if len(config[key]) <= 0:
			errorMsg="Config ["+key+"] is empty"
			log.error(errorMsg)
			raise Exception(errorMsg)
	
	# test if the destination directory exists 
	if not os.path.exists(config["destDir"]):
		errorMsg="The destination directory "+config["destDir"]+" doesn't exists"
		log.error(errorMsg)
		raise Exception(errorMsg)
	

# Method that parse the playlists given and create the music files in the dest directory 
def parsePlaylists(playlists, config):
	
	for playlist in playlists:
		log.info("Parse playlist : %s", playlist["name"])
		
		#directory of the playlist
		playlistDir = config["destDir"] + "/" + playlist["name"].replace("/","")
		
		if not os.path.exists(playlistDir):
			os.makedirs(playlistDir)

		
		#get the tracks of the playlist
		try:
			tracks = jam.getPlaylistTracks(playlist["id"])
		except Exception as e:
			log.exception("Error when trying to get the tracks of the playlist named \"%s\"", playlist["name"])
			continue
		
		tracksPath = []
		
		# parse the tracks and upload those which don't exist 
		for track in tracks:
			
			#track file path
			trackFile = playlistDir + "/" + track["name"].replace("/","") + ".mp3"
			
			tracksPath.append(trackFile)
			
			#if we allready uploaded the file, no need to re-do it
			if(os.path.exists(trackFile)):
				continue
			
			log.info("New track : \"%s\"", track["name"])
			
			
			try:
				urllib.request.urlretrieve(track["audiodownload"], trackFile)
			except Exception as e:
				log.exception("Error when downloading the audio file \"%s\"", track["name"])
				continue
			
		
		# remove the file that don't exists in the playlist
		for trackFile in os.listdir(playlistDir):
			
			trackPath = playlistDir + "/" + trackFile
			
			if trackPath not in tracksPath:
				log.info("Delete track file : %s - no more in the playlist", trackPath)
				os.remove(trackPath)
				

# get the configuration from the config file
config = extractConfig()


jam = JamendoUtil(config["clientId"], config["jamendoUrl"])

#get the id of the user in the config file
try:
	userId = jam.getUserId(config["userName"])
except Exception as e:
	log.exception("Error when trying to get the userId of \"%s\"", config["userName"])
	raise

playlists = []
i = 0
while True:
		
	# get the public playlists of the user
	try:
		currentPlaylists = jam.getPublicPlaylists(userId, playlistLimit, playlistLimit * i)
	except Exception as e:
		log.exception("Error when trying to get public playlists of \"%s\"", config["userName"])
		raise

	playlists.extend(currentPlaylists)

	if len(currentPlaylists) == 0:
		break
	i = i + 1
	


if len(playlists) <= 0:
	log.info("No public playlists for account %s", config["userName"])

log.info("Number of public playlists : %d", len(playlists))

parsePlaylists(playlists, config)
	
	
