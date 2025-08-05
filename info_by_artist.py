'''
Script to print out listening data for a particular artist

usage: python info_by_artist.py [-h] [-a / --artist ARTIST_NAME]

optional arguments:
  -h, --help            show this help message and exit
'''

import numpy as np
import json
import glob
import pandas as pd
import argparse
from collections import Counter


def info_by_artist(artist):
    # TODO: make these params
    directory="/Users/lauranosler/spotify_wrapped/Spotify_Account_Data/"


    # Use glob to find all matching JSON files
    file_pattern = f"{directory}/StreamingHistory_music_*.json"
    json_files = glob.glob(file_pattern)

    # Initialize a list to store the data
    all_data = []
    print("Loading data ...")
    # Read each file and load the JSON content
    for file in json_files:
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_data.extend(data)  # Assuming each file contains a list of entries

    # Now `all_data` contains the combined content of all files
    print(f"Loaded {len(all_data)} records from {len(json_files)} files.")
    print("-------------------------------------------------------")

    # list of dictionaries to store info about each of the songs played
    songs = []
    # Assuming `all_data` is a list of dictionaries loaded from the JSON files

    track_names = [entry['trackName'] for entry in all_data if (('trackName' in entry) and ('artistName' in entry) and (entry["artistName"] == artist))]
    end_times = [pd.to_datetime(entry['endTime']) for entry in all_data if (('endTime' in entry) and ('artistName' in entry) and (entry["artistName"] == artist))]
    ms_played = [entry['msPlayed'] for entry in all_data if (('msPlayed' in entry) and ('artistName' in entry) and (entry["artistName"] == artist))]

    total_time_mins = np.sum(ms_played) / 60000 # convert to minutes

    # Count occurrences of each trackName
    track_counter = Counter(track_names)

    # Top ten tracks
    if (len(track_counter.most_common(1)) > 0):
        most_common_track = track_counter.most_common(1)[0]

        print(f"The most common track by {artist} is '{most_common_track[0]}' with {most_common_track[1]} plays.")


        top_10_tracks = track_counter.most_common(10)

        print("\nTop most played tracks by",artist, ": ")
        for track, count in top_10_tracks:
            print(f"{track}: {count} plays")
    else:
        print("No tracks found for artist ", artist)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--artist', dest="artist_name", help="Artist Name (in quotes)")
    args = vars(parser.parse_args())

    artist = args["artist_name"]
    info_by_artist(artist)