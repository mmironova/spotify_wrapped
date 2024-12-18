import numpy as np
import json
import glob
import pandas as pd
from collections import Counter


directory="/Users/lauranosler/spotify_wrapped/Spotify_Account_Data/"

# Use glob to find all matching JSON files
file_pattern = f"{directory}/StreamingHistory_music_*.json"
json_files = glob.glob(file_pattern)

# Initialize a list to store the data
all_data = []

# Read each file and load the JSON content
for file in json_files:
    with open(file, 'r', encoding='utf-8') as f:
        data = json.load(f)
        all_data.extend(data)  # Assuming each file contains a list of entries

# Now `all_data` contains the combined content of all files
print(f"Loaded {len(all_data)} records from {len(json_files)} files.")

# Assuming `all_data` is a list of dictionaries loaded from the JSON files
artist_names = [entry['artistName'] for entry in all_data if 'artistName' in entry]
end_times = [pd.to_datetime(entry['endTime']) for entry in all_data if 'endTime' in entry]
track_names = [entry['trackName'] for entry in all_data if 'trackName' in entry]
ms_played = [entry['msPlayed'] for entry in all_data if 'msPlayed' in entry]

total_time_mins = np.sum(ms_played) / 60000 # convert to minutes

# Count occurrences of each artistName and trackName
artist_counter = Counter(artist_names)
track_counter = Counter(track_names)

# Find the most common artistName and trackName
most_common_artist = artist_counter.most_common(1)[0]  # Gets the top artist
most_common_track = track_counter.most_common(1)[0]

print(f"The most common artist is '{most_common_artist[0]}' with {most_common_artist[1]} plays.")
print(f"The most common track is '{most_common_track[0]}' with {most_common_track[1]} plays.")

# Optionally, print the top 10 most common artists
top_10_artists = artist_counter.most_common(10)
top_10_tracks = track_counter.most_common(10)

print("\nTop 10 most common artists:")
for artist, count in top_10_artists:
    print(f"{artist}: {count} plays")

print("\nTop 10 most common tracks:")
for track, count in top_10_tracks:
    print(f"{track}: {count} plays")

print(f"Total number minutes listened: {total_time_mins}")
