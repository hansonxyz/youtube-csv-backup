# YouTube CSV Editor

This repository contains two programs, `youtube-get.py` and `youtube-set.py`, for editing YouTube playlists.

## Installation

To use these programs, you need to install the following Python packages:

`pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client and pandas`

You also need to set up a Google Cloud project, create a "desktop application", and enable the YouTube API v3. You then need to create an OAuth client token and save it as `client_secrets.json` in the same directory as the scripts.

## Usage

1. Run `youtube-get.py` to retrieve the contents of all your playlists. The playlists will be stored in the `playlists` directory.

2. Modify a playlist as desired.

3. Run `youtube-set.py (filename)` to update the playlist with the contents of your modified CSV file.
