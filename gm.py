#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json,re
from gmusicapi import Mobileclient
from pathlib import Path
from collections import Counter,deque

mc = Mobileclient()
mc.login('hisaruki@gmail.com', 'LiAlSi8O20', Mobileclient.FROM_MAC_ADDRESS)
"""
songs = mc.get_all_songs()
with Path("songs.json").open("w") as f:
  f.write(json.dumps(songs))
"""

with Path("songs.json").open("r") as f:
  songs = json.loads(f.read())



for song in deque(songs,1000):
  if re.search(u'ラルク|(?=.*arc)(?=.*en)(?=.*ciel)',song["artist"].lower()) and song["artist"] != 'L\'Arc~en~Ciel' and song["albumArtist"] != "Various":
    #print(song["title"],song["artist"],song["albumArtist"])
    song["artist"] = 'L\'Arc~en~Ciel'
    song["albumArtist"] = 'L\'Arc~en~Ciel'
    print(song)
    print( mc.change_song_metadata(song) )