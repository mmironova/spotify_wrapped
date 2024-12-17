import numpy as np
import json
import glob
from collections import Counter


directory="/Users/mironova/Documents/spotify2024/laura_spotify_data/"

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
artist_names = [entry['trackName'] for entry in all_data if 'trackName' in entry]

# Count occurrences of each artistName
artist_counter = Counter(artist_names)

# Find the most common artistName
most_common_artist = artist_counter.most_common(1)[0]  # Gets the top artist
print(f"The most common track is '{most_common_artist[0]}' with {most_common_artist[1]} plays.")

# Optionally, print the top 10 most common artists
top_10_artists = artist_counter.most_common(10)
print("\nTop 10 most common track:")
for artist, count in top_10_artists:
    print(f"{artist}: {count} plays")
