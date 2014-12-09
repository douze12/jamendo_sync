jamendo_sync
============

Python script which synchonize the public Jamendo playlists in a local directory.

# Use

Before using it, you need to change the configuration file named ```conf``` with the following properties : 
- jamendoUrl : URL of the jamendo API. Do not change.
- clientId : Client ID needed to use the Jamendo API. Do not change.
- userName : The name of the Jamendo user
- destDir : Path of the directory where the music files will be uploaded

Then, you can call the program by launching:
```bash
$ python3 jamendo_sync.py
```

The script will create a directory for each public playlist available with the name of the playlist and will upload the tracks in this directory.

A log file ```.log``` will be created in the same directory than the python script. 
