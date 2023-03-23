Youtube CSV editor

This repository has two programs - youtube-get.py and youtube-set.py.

To use this program, first install the following python packages:

pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client and pandas

Next, go to your Google Cloud project console, create a 'desktop application', enable the youtube API v3, then create a oauth client token.  Save the token as client_secrets.json in the same directory as these scripts.

Run youtube-get.py to get the contents of all your playlists.  They will be stored in the directory playlists.

After modifying a playlist, run youtube-set.py (filename) to update a playlist with the contents of your modified CSV.
