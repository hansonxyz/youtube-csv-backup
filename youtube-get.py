import os
import re
import csv
import json
import pandas as pd
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Set your API key file and scopes
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
CLIENT_SECRETS_FILE = 'client_secrets.json'
SCOPES = ['https://www.googleapis.com/auth/youtube']

def get_authenticated_service():
    token_file = 'token.txt'

    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri='urn:ietf:wg:oauth:2.0:oob'
    )

    credentials = None

    if os.path.exists(token_file):
       credentials = Credentials.from_authorized_user_file(token_file, SCOPES)

    else:

        auth_url, _ = flow.authorization_url(prompt='consent')
        print('Please go to this URL: {}'.format(auth_url))
        code = input('Enter the authorization code: ')
        flow.fetch_token(code=code)

        credentials = flow.credentials

        # Save the token to token.txt
        with open(token_file, 'w') as f:
            f.write(credentials.to_json())

    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def get_playlists(youtube):
    request = youtube.playlists().list(
        part='snippet',
        mine=True,
        maxResults=50
    )
    response = request.execute()
    return response

def export_playlists_to_csv(playlists, youtube):
    for item in playlists['items']:
        playlist_id = item['id']
        title = item['snippet']['title']
        videos = get_videos_in_playlist(playlist_id, youtube)
        export_playlist_to_csv(playlist_id, title, videos)

def export_playlist_to_csv(playlist_id, title, videos):
    if not os.path.exists('playlists'):
        os.makedirs('playlists')
    title = re.sub(r'[^a-zA-Z0-9\s\-]', '', title)
    filename = f"playlists/{playlist_id}-{title}.csv"
    df = pd.DataFrame(videos, columns=['Title', 'Description', 'ID', 'URL'])
    df.to_csv(filename, index=False)
    print(f"Playlist '{title}' exported to '{filename}'")

def get_videos_in_playlist(playlist_id, youtube):
    videos = []
    next_page_token = None
    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            playlistId=playlist_id,
            maxResults=50,
            pageToken=next_page_token
        )
        response = request.execute()
        for item in response['items']:
            video_id = item['snippet']['resourceId']['videoId']
            title = item['snippet']['title']
            description = item['snippet']['description']
            url = 'https://www.youtube.com/watch?v='+video_id
            videos.append([title, description, video_id, url])
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break
    return videos
    
def main():
    try:
        youtube = get_authenticated_service()
        playlists = get_playlists(youtube)
        export_playlists_to_csv(playlists, youtube)
    except HttpError as error:
        print(f'An error occurred: {error}')
        playlists = None

if __name__ == '__main__':
    main()
