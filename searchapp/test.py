import json
import os
import textwrap

dir_path = os.path.dirname(os.path.realpath(__file__))
songs_path = os.path.join(dir_path, 'songs.json')
with open(songs_path) as song_file:
    for idx, song in enumerate(json.load(song_file, strict=False)):
        id_ = idx + 1  # ES indexes must be positive integers, so add 1
        print(song)