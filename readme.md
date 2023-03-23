# YouTube CSV Backup and Restore

This repository contains two programs, `youtube-get.py` and `youtube-set.py`, for editing YouTube playlists.

## Installation

To use these programs, you need to install the following Python packages:

`pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client and pandas`

You also need to set up a Google Cloud project, create a "desktop application", and enable the YouTube API v3. You then need to create an OAuth client token and save it as `client_secrets.json` in the same directory as the scripts.

## Backup Usage

Run youtube-get.py to export your Youtube playlists as CSV files:

python youtube-get.py

This will create a CSV file for each playlist in the playlists directory.

To restore a playlist from a CSV file, run youtube-set.py with the path to the CSV file as an argument:

python youtube-set.py /path/to/your/csv_file.csv

Replace /path/to/your/csv_file.csv with the actual path to the CSV file.
